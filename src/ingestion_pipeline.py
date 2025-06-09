"""Ingestion pipeline for processing JAR files and building the knowledge base."""

import logging
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

from src.config import settings
from src.jar_processor import JarProcessor
from src.vector_db import VectorDatabase
from src.java_parser import CodeChunk

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IngestionPipeline:
    """Pipeline for ingesting JAR files and building the knowledge base."""
    
    def __init__(self, collection_name: str = "java_code_chunks"):
        """Initialize the ingestion pipeline."""
        self.jar_processor = JarProcessor()
        self.vector_db = VectorDatabase(collection_name)
        self.collection_name = collection_name
    
    def ingest_jar_file(self, jar_path: Path, reset_collection: bool = False) -> Dict[str, Any]:
        """Ingest a single JAR file into the knowledge base."""
        logger.info(f"Starting ingestion of JAR file: {jar_path}")
        start_time = time.time()
        
        # Validate JAR file
        if not self.jar_processor.validate_jar_file(jar_path):
            return {
                "success": False,
                "error": f"Invalid JAR file: {jar_path}",
                "chunks_processed": 0,
                "processing_time": 0
            }
        
        # Reset collection if requested
        if reset_collection:
            logger.info("Resetting vector database collection")
            self.vector_db.reset_collection()
        
        try:
            # Extract and parse code chunks
            logger.info("Extracting and parsing Java code...")
            chunks = self.jar_processor.process_jar_file(jar_path)
            
            if not chunks:
                return {
                    "success": False,
                    "error": "No code chunks extracted from JAR file",
                    "chunks_processed": 0,
                    "processing_time": time.time() - start_time
                }
            
            # Add chunks to vector database
            logger.info("Adding chunks to vector database...")
            self.vector_db.add_chunks(chunks)
            
            processing_time = time.time() - start_time
            
            # Get JAR metadata
            jar_metadata = self.jar_processor.get_jar_metadata(jar_path)
            
            result = {
                "success": True,
                "jar_file": str(jar_path),
                "chunks_processed": len(chunks),
                "processing_time": processing_time,
                "jar_metadata": jar_metadata,
                "chunk_statistics": self._analyze_chunks(chunks)
            }
            
            logger.info(f"Successfully ingested {len(chunks)} chunks in {processing_time:.2f} seconds")
            return result
            
        except Exception as e:
            logger.error(f"Error during ingestion: {e}")
            return {
                "success": False,
                "error": str(e),
                "chunks_processed": 0,
                "processing_time": time.time() - start_time
            }
    
    def ingest_jar_directory(self, jar_dir: Path, reset_collection: bool = False) -> Dict[str, Any]:
        """Ingest all JAR files in a directory."""
        logger.info(f"Starting ingestion of JAR directory: {jar_dir}")
        start_time = time.time()
        
        if not jar_dir.exists() or not jar_dir.is_dir():
            return {
                "success": False,
                "error": f"Directory not found: {jar_dir}",
                "files_processed": 0,
                "total_chunks": 0,
                "processing_time": 0
            }
        
        # Find all JAR files
        jar_files = list(jar_dir.glob('**/*-sources.jar'))
        
        if not jar_files:
            return {
                "success": False,
                "error": f"No sources JAR files found in {jar_dir}",
                "files_processed": 0,
                "total_chunks": 0,
                "processing_time": 0
            }
        
        logger.info(f"Found {len(jar_files)} JAR files to process")
        
        # Reset collection if requested (only for the first file)
        if reset_collection:
            logger.info("Resetting vector database collection")
            self.vector_db.reset_collection()
        
        # Process each JAR file
        results = []
        total_chunks = 0
        successful_files = 0
        
        for i, jar_file in enumerate(jar_files, 1):
            logger.info(f"Processing JAR {i}/{len(jar_files)}: {jar_file.name}")
            
            result = self.ingest_jar_file(jar_file, reset_collection=False)
            results.append(result)
            
            if result["success"]:
                successful_files += 1
                total_chunks += result["chunks_processed"]
            else:
                logger.error(f"Failed to process {jar_file}: {result.get('error', 'Unknown error')}")
        
        processing_time = time.time() - start_time
        
        return {
            "success": successful_files > 0,
            "directory": str(jar_dir),
            "files_found": len(jar_files),
            "files_processed": successful_files,
            "files_failed": len(jar_files) - successful_files,
            "total_chunks": total_chunks,
            "processing_time": processing_time,
            "detailed_results": results
        }
    
    def ingest_batch(self, jar_paths: List[Path], reset_collection: bool = False) -> Dict[str, Any]:
        """Ingest a batch of JAR files."""
        logger.info(f"Starting batch ingestion of {len(jar_paths)} JAR files")
        start_time = time.time()
        
        # Reset collection if requested
        if reset_collection:
            logger.info("Resetting vector database collection")
            self.vector_db.reset_collection()
        
        # Process all JAR files
        all_chunks = []
        successful_files = 0
        failed_files = []
        
        for i, jar_path in enumerate(jar_paths, 1):
            logger.info(f"Processing JAR {i}/{len(jar_paths)}: {jar_path.name}")
            
            try:
                if self.jar_processor.validate_jar_file(jar_path):
                    chunks = self.jar_processor.process_jar_file(jar_path)
                    all_chunks.extend(chunks)
                    successful_files += 1
                    logger.info(f"Extracted {len(chunks)} chunks from {jar_path.name}")
                else:
                    failed_files.append(str(jar_path))
                    logger.error(f"Invalid JAR file: {jar_path}")
            except Exception as e:
                failed_files.append(str(jar_path))
                logger.error(f"Error processing {jar_path}: {e}")
        
        # Add all chunks to vector database in one batch
        if all_chunks:
            logger.info(f"Adding {len(all_chunks)} total chunks to vector database...")
            self.vector_db.add_chunks(all_chunks)
        
        processing_time = time.time() - start_time
        
        return {
            "success": successful_files > 0,
            "files_processed": successful_files,
            "files_failed": len(failed_files),
            "failed_files": failed_files,
            "total_chunks": len(all_chunks),
            "processing_time": processing_time,
            "chunk_statistics": self._analyze_chunks(all_chunks) if all_chunks else {}
        }
    
    def get_ingestion_status(self) -> Dict[str, Any]:
        """Get the current status of the knowledge base."""
        stats = self.vector_db.get_collection_stats()
        
        return {
            "collection_name": self.collection_name,
            "total_chunks": stats["total_chunks"],
            "chunk_types": stats["chunk_types"],
            "unique_source_files": stats["unique_source_files"],
            "unique_classes": stats["unique_classes"],
            "ready_for_queries": stats["total_chunks"] > 0
        }
    
    def validate_sources_directory(self, sources_dir: Path) -> Dict[str, Any]:
        """Validate a sources directory and provide recommendations."""
        if not sources_dir.exists():
            return {
                "valid": False,
                "error": f"Directory does not exist: {sources_dir}",
                "recommendations": ["Create the directory and add JAR files"]
            }
        
        if not sources_dir.is_dir():
            return {
                "valid": False,
                "error": f"Path is not a directory: {sources_dir}",
                "recommendations": ["Provide a valid directory path"]
            }
        
        # Find JAR files
        jar_files = list(sources_dir.glob('**/*-sources.jar'))
        all_jar_files = list(sources_dir.glob('**/*.jar'))
        
        recommendations = []
        
        if not jar_files:
            if all_jar_files:
                recommendations.append(f"Found {len(all_jar_files)} JAR files, but none are sources JARs (-sources.jar)")
                recommendations.append("Ensure you have the source versions of your dependencies")
            else:
                recommendations.append("No JAR files found in directory")
                recommendations.append("Add JAR files with source code to this directory")
        
        # Validate each JAR file
        valid_jars = []
        invalid_jars = []
        
        for jar_file in jar_files:
            if self.jar_processor.validate_jar_file(jar_file):
                valid_jars.append(jar_file)
            else:
                invalid_jars.append(jar_file)
        
        if invalid_jars:
            recommendations.append(f"Found {len(invalid_jars)} invalid JAR files")
        
        return {
            "valid": len(valid_jars) > 0,
            "total_jar_files": len(all_jar_files),
            "sources_jar_files": len(jar_files),
            "valid_sources_jars": len(valid_jars),
            "invalid_jars": len(invalid_jars),
            "recommendations": recommendations,
            "valid_jar_files": [str(jar) for jar in valid_jars[:10]],  # Show first 10
            "invalid_jar_files": [str(jar) for jar in invalid_jars[:5]]   # Show first 5
        }
    
    def _analyze_chunks(self, chunks: List[CodeChunk]) -> Dict[str, Any]:
        """Analyze code chunks and provide statistics."""
        if not chunks:
            return {}
        
        chunk_types = {}
        classes = set()
        source_files = set()
        total_lines = 0
        
        for chunk in chunks:
            # Count chunk types
            chunk_type = chunk.chunk_type
            chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1
            
            # Collect unique classes and files
            if chunk.class_name:
                classes.add(chunk.class_name)
            
            source_files.add(chunk.source_file)
            
            # Count lines
            total_lines += chunk.end_line - chunk.start_line + 1
        
        return {
            "chunk_types": chunk_types,
            "unique_classes": len(classes),
            "unique_source_files": len(source_files),
            "total_lines_of_code": total_lines,
            "average_chunk_size": total_lines / len(chunks) if chunks else 0
        }
    
    def cleanup_temp_files(self) -> None:
        """Clean up temporary files created during processing."""
        temp_dir = settings.temp_dir
        if temp_dir.exists():
            import shutil
            shutil.rmtree(temp_dir)
            temp_dir.mkdir(exist_ok=True)
            logger.info("Cleaned up temporary files")