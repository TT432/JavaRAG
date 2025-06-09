"""JAR file processor for extracting Java source files."""

import logging
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import List, Generator

from .config import settings
from .java_parser import JavaParser, CodeChunk

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JarProcessor:
    """Processor for handling JAR files and extracting Java source code."""
    
    def __init__(self):
        """Initialize the JAR processor."""
        self.java_parser = JavaParser()
        self.temp_dir = settings.temp_dir
    
    def process_jar_file(self, jar_path: Path) -> List[CodeChunk]:
        """Process a single JAR file and extract code chunks."""
        logger.info(f"Processing JAR file: {jar_path}")
        
        if not jar_path.exists():
            logger.error(f"JAR file not found: {jar_path}")
            return []
        
        if not jar_path.name.endswith('-sources.jar'):
            logger.warning(f"File {jar_path} is not a sources JAR file")
        
        chunks = []
        
        # Create a temporary directory for extraction
        with tempfile.TemporaryDirectory(dir=self.temp_dir) as temp_extract_dir:
            try:
                # Extract JAR file
                extracted_files = self._extract_jar(jar_path, Path(temp_extract_dir))
                
                # Process each Java file
                for java_file in extracted_files:
                    file_chunks = self.java_parser.parse_file(java_file)
                    chunks.extend(file_chunks)
                
                logger.info(f"Extracted {len(chunks)} code chunks from {jar_path}")
                
            except Exception as e:
                logger.error(f"Error processing JAR file {jar_path}: {e}")
        
        return chunks
    
    def process_jar_directory(self, jar_dir: Path) -> List[CodeChunk]:
        """Process all JAR files in a directory."""
        logger.info(f"Processing JAR directory: {jar_dir}")
        
        if not jar_dir.exists() or not jar_dir.is_dir():
            logger.error(f"Directory not found: {jar_dir}")
            return []
        
        all_chunks = []
        jar_files = list(jar_dir.glob('**/*-sources.jar'))
        
        if not jar_files:
            logger.warning(f"No sources JAR files found in {jar_dir}")
            return []
        
        logger.info(f"Found {len(jar_files)} sources JAR files")
        
        for jar_file in jar_files:
            chunks = self.process_jar_file(jar_file)
            all_chunks.extend(chunks)
        
        logger.info(f"Total extracted chunks: {len(all_chunks)}")
        return all_chunks
    
    def _extract_jar(self, jar_path: Path, extract_dir: Path) -> List[Path]:
        """Extract JAR file and return list of Java files."""
        java_files = []
        
        try:
            with zipfile.ZipFile(jar_path, 'r') as jar_file:
                # Extract all files
                jar_file.extractall(extract_dir)
                
                # Find all Java files
                for java_file in extract_dir.rglob('*.java'):
                    if java_file.is_file():
                        java_files.append(java_file)
                
                logger.debug(f"Extracted {len(java_files)} Java files from {jar_path}")
                
        except zipfile.BadZipFile:
            logger.error(f"Invalid ZIP/JAR file: {jar_path}")
        except Exception as e:
            logger.error(f"Error extracting JAR file {jar_path}: {e}")
        
        return java_files
    
    def get_jar_metadata(self, jar_path: Path) -> dict:
        """Extract metadata from JAR file."""
        metadata = {
            'jar_name': jar_path.name,
            'jar_path': str(jar_path),
            'size_bytes': jar_path.stat().st_size if jar_path.exists() else 0,
            'java_file_count': 0,
            'manifest_info': {}
        }
        
        try:
            with zipfile.ZipFile(jar_path, 'r') as jar_file:
                # Count Java files
                java_files = [name for name in jar_file.namelist() if name.endswith('.java')]
                metadata['java_file_count'] = len(java_files)
                
                # Extract manifest information
                try:
                    manifest_content = jar_file.read('META-INF/MANIFEST.MF').decode('utf-8')
                    manifest_lines = manifest_content.strip().split('\n')
                    
                    for line in manifest_lines:
                        if ':' in line:
                            key, value = line.split(':', 1)
                            metadata['manifest_info'][key.strip()] = value.strip()
                            
                except KeyError:
                    logger.debug(f"No manifest found in {jar_path}")
                
        except Exception as e:
            logger.error(f"Error reading JAR metadata from {jar_path}: {e}")
        
        return metadata
    
    def validate_jar_file(self, jar_path: Path) -> bool:
        """Validate that a JAR file is a valid sources JAR."""
        if not jar_path.exists():
            logger.error(f"JAR file does not exist: {jar_path}")
            return False
        
        if not jar_path.name.endswith('-sources.jar'):
            logger.warning(f"File {jar_path} is not a sources JAR file")
            return False
        
        try:
            with zipfile.ZipFile(jar_path, 'r') as jar_file:
                # Check if it contains Java files
                java_files = [name for name in jar_file.namelist() if name.endswith('.java')]
                
                if not java_files:
                    logger.warning(f"No Java files found in {jar_path}")
                    return False
                
                logger.info(f"Valid sources JAR: {jar_path} ({len(java_files)} Java files)")
                return True
                
        except zipfile.BadZipFile:
            logger.error(f"Invalid ZIP/JAR file: {jar_path}")
            return False
        except Exception as e:
            logger.error(f"Error validating JAR file {jar_path}: {e}")
            return False
    
    def list_jar_contents(self, jar_path: Path) -> List[str]:
        """List all Java files in a JAR."""
        java_files = []
        
        try:
            with zipfile.ZipFile(jar_path, 'r') as jar_file:
                java_files = [name for name in jar_file.namelist() if name.endswith('.java')]
                java_files.sort()
                
        except Exception as e:
            logger.error(f"Error listing JAR contents {jar_path}: {e}")
        
        return java_files