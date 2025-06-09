"""Vector database manager using ChromaDB for code embeddings."""

import logging
import uuid
from typing import List, Dict, Any, Optional

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from .config import settings
from .java_parser import CodeChunk

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorDatabase:
    """Vector database manager for storing and retrieving code embeddings."""
    
    def __init__(self, collection_name: str = "java_code_chunks"):
        """Initialize the vector database."""
        self.collection_name = collection_name
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Initialize embedding model
        logger.info(f"Loading embedding model: {settings.embedding_model}")
        self.embedding_model = SentenceTransformer(settings.embedding_model)
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
            logger.info(f"Loaded existing collection: {collection_name}")
        except Exception:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"description": "Java code chunks for RAG"}
            )
            logger.info(f"Created new collection: {collection_name}")
    
    def add_chunks(self, chunks: List[CodeChunk]) -> None:
        """Add code chunks to the vector database."""
        if not chunks:
            logger.warning("No chunks to add")
            return
        
        logger.info(f"Adding {len(chunks)} chunks to vector database")
        
        # Prepare data for batch insertion
        documents = []
        metadatas = []
        ids = []
        
        for chunk in chunks:
            # Create document text for embedding
            doc_text = self._create_document_text(chunk)
            documents.append(doc_text)
            
            # Create metadata
            metadata = {
                "source_file": chunk.source_file,
                "class_name": chunk.class_name or "",
                "method_name": chunk.method_name or "",
                "start_line": chunk.start_line,
                "end_line": chunk.end_line,
                "chunk_type": chunk.chunk_type,
                "content": chunk.content,
                **chunk.metadata
            }
            
            # Convert lists to strings for ChromaDB compatibility
            for key, value in metadata.items():
                if isinstance(value, list):
                    metadata[key] = ", ".join(str(v) for v in value)
                elif value is None:
                    metadata[key] = ""
                else:
                    metadata[key] = str(value)
            
            metadatas.append(metadata)
            
            # Generate unique ID
            chunk_id = self._generate_chunk_id(chunk)
            ids.append(chunk_id)
        
        # Generate embeddings
        logger.info("Generating embeddings...")
        embeddings = self.embedding_model.encode(documents).tolist()
        
        # Add to collection in batches
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            end_idx = min(i + batch_size, len(documents))
            
            self.collection.add(
                documents=documents[i:end_idx],
                metadatas=metadatas[i:end_idx],
                ids=ids[i:end_idx],
                embeddings=embeddings[i:end_idx]
            )
            
            logger.debug(f"Added batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1}")
        
        logger.info(f"Successfully added {len(chunks)} chunks to vector database")
    
    def search(self, query: str, top_k: int = 5, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for relevant code chunks."""
        logger.info(f"Searching for: '{query}' (top_k={top_k})")
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query]).tolist()[0]
        
        # Prepare where clause for filtering
        where_clause = None
        if filters:
            where_clause = {}
            for key, value in filters.items():
                if value:  # Only add non-empty filters
                    where_clause[key] = {"$eq": str(value)}
        
        # Search the collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_clause,
            include=["documents", "metadatas", "distances"]
        )
        
        # Format results
        formatted_results = []
        if results['documents'] and results['documents'][0]:
            for i, (doc, metadata, distance) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )):
                formatted_results.append({
                    "rank": i + 1,
                    "content": metadata.get("content", doc),
                    "source_file": metadata.get("source_file", ""),
                    "class_name": metadata.get("class_name", ""),
                    "method_name": metadata.get("method_name", ""),
                    "chunk_type": metadata.get("chunk_type", ""),
                    "start_line": metadata.get("start_line", ""),
                    "end_line": metadata.get("end_line", ""),
                    "similarity_score": 1 - distance,  # Convert distance to similarity
                    "metadata": metadata
                })
        
        logger.info(f"Found {len(formatted_results)} relevant chunks")
        return formatted_results
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        count = self.collection.count()
        
        # Get sample of metadata to understand the data
        sample_results = self.collection.get(
            limit=min(100, count),
            include=["metadatas"]
        )
        
        # Analyze chunk types
        chunk_types = {}
        source_files = set()
        classes = set()
        
        if sample_results['metadatas']:
            for metadata in sample_results['metadatas']:
                chunk_type = metadata.get('chunk_type', 'unknown')
                chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1
                
                if metadata.get('source_file'):
                    source_files.add(metadata['source_file'])
                
                if metadata.get('class_name'):
                    classes.add(metadata['class_name'])
        
        return {
            "total_chunks": count,
            "chunk_types": chunk_types,
            "unique_source_files": len(source_files),
            "unique_classes": len(classes),
            "collection_name": self.collection_name
        }
    
    def delete_collection(self) -> None:
        """Delete the entire collection."""
        logger.warning(f"Deleting collection: {self.collection_name}")
        self.client.delete_collection(name=self.collection_name)
    
    def reset_collection(self) -> None:
        """Reset the collection (delete and recreate)."""
        logger.warning(f"Resetting collection: {self.collection_name}")
        try:
            self.client.delete_collection(name=self.collection_name)
        except ValueError:
            pass  # Collection doesn't exist
        
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"description": "Java code chunks for RAG"}
        )
        logger.info(f"Reset collection: {self.collection_name}")
    
    def _create_document_text(self, chunk: CodeChunk) -> str:
        """Create searchable document text from a code chunk."""
        # Combine different aspects of the code for better searchability
        parts = []
        
        # Add class and method context
        if chunk.class_name:
            parts.append(f"Class: {chunk.class_name}")
        
        if chunk.method_name:
            parts.append(f"Method: {chunk.method_name}")
        
        # Add chunk type
        parts.append(f"Type: {chunk.chunk_type}")
        
        # Add the actual code content
        parts.append(f"Code:\n{chunk.content}")
        
        # Add metadata as searchable text
        if chunk.metadata:
            metadata_text = []
            for key, value in chunk.metadata.items():
                if value and key not in ['content']:  # Avoid duplicating content
                    if isinstance(value, list):
                        metadata_text.append(f"{key}: {', '.join(str(v) for v in value)}")
                    else:
                        metadata_text.append(f"{key}: {value}")
            
            if metadata_text:
                parts.append(f"Metadata: {'; '.join(metadata_text)}")
        
        return "\n\n".join(parts)
    
    def _generate_chunk_id(self, chunk: CodeChunk) -> str:
        """Generate a unique ID for a code chunk."""
        # Create a deterministic ID based on chunk content and location
        base_string = f"{chunk.source_file}:{chunk.start_line}:{chunk.end_line}:{chunk.chunk_type}"
        
        if chunk.class_name:
            base_string += f":{chunk.class_name}"
        
        if chunk.method_name:
            base_string += f":{chunk.method_name}"
        
        # Use UUID5 for deterministic ID generation
        namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')  # DNS namespace
        return str(uuid.uuid5(namespace, base_string))