"""RAG service for answering queries about Java code."""

import logging
from typing import List, Dict, Any, Optional

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate

from .config import settings
from .vector_db import VectorDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGService:
    """RAG service for answering queries about Java code."""
    
    def __init__(self, collection_name: str = "java_code_chunks"):
        """Initialize the RAG service."""
        self.vector_db = VectorDatabase(collection_name)
        
        # Initialize LLM
        if not settings.openai_api_key:
            logger.warning("OpenAI API key not found. LLM functionality will be limited.")
            self.llm = None
        else:
            self.llm = ChatOpenAI(
                api_key=settings.openai_api_key,
                base_url=settings.openai_api_base,
                model=settings.openai_model,
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens
            )
        
        # Define the prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["context", "query"],
            template="""You are a helpful assistant that answers questions about Java code based on provided source code context.

Context (Java source code):
---
{context}
---

Question: {query}

Instructions:
1. Answer the question based ONLY on the provided source code context above.
2. If the context doesn't contain enough information to answer the question, say so explicitly.
3. Include relevant code snippets in your answer when helpful.
4. Provide specific class names, method names, and line references when available.
5. Be precise and technical in your explanations.
6. Do not make assumptions or add information not present in the context.

Answer:"""
        )
    
    def query(self, 
              user_query: str, 
              top_k: int = 5, 
              filters: Optional[Dict[str, Any]] = None,
              include_metadata: bool = False) -> Dict[str, Any]:
        """Process a user query and return an answer."""
        logger.info(f"Processing query: '{user_query}'")
        
        # Step 1: Retrieve relevant code chunks
        retrieved_chunks = self.vector_db.search(
            query=user_query,
            top_k=top_k,
            filters=filters
        )
        
        if not retrieved_chunks:
            return {
                "answer": "No relevant code found for your query.",
                "retrieved_chunks": [],
                "metadata": {
                    "query": user_query,
                    "chunks_found": 0,
                    "llm_used": False
                }
            }
        
        # Step 2: Prepare context from retrieved chunks
        context = self._format_context(retrieved_chunks)
        
        # Step 3: Generate answer using LLM
        if self.llm:
            try:
                answer = self._generate_answer(user_query, context)
                llm_used = True
            except Exception as e:
                logger.error(f"Error generating LLM answer: {e}")
                answer = self._fallback_answer(user_query, retrieved_chunks)
                llm_used = False
        else:
            answer = self._fallback_answer(user_query, retrieved_chunks)
            llm_used = False
        
        # Prepare response
        response = {
            "answer": answer,
            "retrieved_chunks": retrieved_chunks if include_metadata else [],
            "metadata": {
                "query": user_query,
                "chunks_found": len(retrieved_chunks),
                "llm_used": llm_used,
                "top_k": top_k,
                "filters": filters or {}
            }
        }
        
        logger.info(f"Query processed successfully. Found {len(retrieved_chunks)} relevant chunks.")
        return response
    
    def search_code(self, 
                   query: str, 
                   top_k: int = 10, 
                   filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for code chunks without LLM generation."""
        logger.info(f"Searching code for: '{query}'")
        
        results = self.vector_db.search(
            query=query,
            top_k=top_k,
            filters=filters
        )
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base."""
        return self.vector_db.get_collection_stats()
    
    def _format_context(self, chunks: List[Dict[str, Any]]) -> str:
        """Format retrieved chunks into context for the LLM."""
        context_parts = []
        
        for i, chunk in enumerate(chunks, 1):
            # Create a formatted context entry
            context_entry = f"""[Chunk {i}]
File: {chunk['source_file']}
Class: {chunk['class_name']}
Method: {chunk['method_name']}
Type: {chunk['chunk_type']}
Lines: {chunk['start_line']}-{chunk['end_line']}
Similarity: {chunk['similarity_score']:.3f}

Code:
{chunk['content']}
"""
            context_parts.append(context_entry)
        
        return "\n" + "="*80 + "\n".join(context_parts)
    
    def _generate_answer(self, query: str, context: str) -> str:
        """Generate an answer using the LLM."""
        # Create the prompt
        prompt = self.prompt_template.format(context=context, query=query)
        
        # Generate response
        messages = [HumanMessage(content=prompt)]
        response = self.llm(messages)
        
        return response.content.strip()
    
    def _fallback_answer(self, query: str, chunks: List[Dict[str, Any]]) -> str:
        """Generate a fallback answer when LLM is not available."""
        if not chunks:
            return "No relevant code found for your query."
        
        # Create a simple formatted response
        answer_parts = [
            f"Found {len(chunks)} relevant code chunks for your query:",
            ""
        ]
        
        for i, chunk in enumerate(chunks[:3], 1):  # Show top 3 chunks
            chunk_info = f"""**{i}. {chunk['chunk_type'].title()}**: {chunk['method_name'] or chunk['class_name']}
   - File: {chunk['source_file']}
   - Lines: {chunk['start_line']}-{chunk['end_line']}
   - Similarity: {chunk['similarity_score']:.3f}
   
   ```java
   {chunk['content'][:500]}{'...' if len(chunk['content']) > 500 else ''}
   ```
"""
            answer_parts.append(chunk_info)
        
        if len(chunks) > 3:
            answer_parts.append(f"\n... and {len(chunks) - 3} more relevant chunks.")
        
        answer_parts.append("\n*Note: LLM is not available. Showing raw search results.*")
        
        return "\n".join(answer_parts)
    
    def suggest_filters(self, query: str) -> Dict[str, List[str]]:
        """Suggest possible filters based on the query and available data."""
        # Get a sample of data to understand available filters
        sample_results = self.vector_db.search(query, top_k=20)
        
        suggestions = {
            "class_names": [],
            "chunk_types": [],
            "source_files": []
        }
        
        for result in sample_results:
            if result['class_name'] and result['class_name'] not in suggestions["class_names"]:
                suggestions["class_names"].append(result['class_name'])
            
            if result['chunk_type'] and result['chunk_type'] not in suggestions["chunk_types"]:
                suggestions["chunk_types"].append(result['chunk_type'])
            
            if result['source_file'] and result['source_file'] not in suggestions["source_files"]:
                suggestions["source_files"].append(result['source_file'])
        
        # Limit suggestions
        for key in suggestions:
            suggestions[key] = suggestions[key][:10]
        
        return suggestions
    
    def health_check(self) -> Dict[str, Any]:
        """Perform a health check of the RAG service."""
        health = {
            "status": "healthy",
            "issues": [],
            "components": {}
        }
        
        # Check vector database
        try:
            stats = self.vector_db.get_collection_stats()
            health["components"]["vector_db"] = {
                "status": "healthy",
                "total_chunks": stats["total_chunks"]
            }
            
            if stats["total_chunks"] == 0:
                health["issues"].append("No code chunks in vector database")
                health["status"] = "warning"
                
        except Exception as e:
            health["components"]["vector_db"] = {
                "status": "error",
                "error": str(e)
            }
            health["issues"].append(f"Vector database error: {e}")
            health["status"] = "error"
        
        # Check LLM
        if self.llm:
            try:
                # Simple test query
                test_response = self.llm([HumanMessage(content="Hello")])
                health["components"]["llm"] = {
                    "status": "healthy",
                    "model": "gpt-4"
                }
            except Exception as e:
                health["components"]["llm"] = {
                    "status": "error",
                    "error": str(e)
                }
                health["issues"].append(f"LLM error: {e}")
                if health["status"] != "error":
                    health["status"] = "warning"
        else:
            health["components"]["llm"] = {
                "status": "disabled",
                "reason": "No OpenAI API key configured"
            }
            health["issues"].append("LLM not available - no API key")
            if health["status"] == "healthy":
                health["status"] = "warning"
        
        return health