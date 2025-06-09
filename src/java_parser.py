"""Java code parser using Tree-sitter for intelligent code chunking."""

import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

import tree_sitter
from tree_sitter import Language, Parser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CodeChunk:
    """Represents a semantic chunk of Java code."""
    content: str
    source_file: str
    class_name: Optional[str]
    method_name: Optional[str]
    start_line: int
    end_line: int
    chunk_type: str  # 'method', 'class', 'interface', 'field'
    metadata: Dict[str, Any]

class JavaParser:
    """Parser for Java source code using Tree-sitter."""
    
    def __init__(self):
        """Initialize the Java parser."""
        try:
            # Try to use tree-sitter-java installed via pip
            import tree_sitter_java as tsjava
            self.java_language = Language(tsjava.language())
        except ImportError:
            try:
                # Fallback: try to build from source
                self.java_language = Language(
                    tree_sitter.Language.build_library(
                        'build/java.so',
                        ['tree-sitter-java']
                    )
                )
            except Exception:
                logger.error("Tree-sitter Java language not found. Please install tree-sitter-java.")
                raise
        
        self.parser = Parser()
        self.parser.language = self.java_language
    
    def parse_file(self, file_path: Path) -> List[CodeChunk]:
        """Parse a Java file and extract semantic chunks."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            return self.parse_java_code(source_code, str(file_path))
            
        except Exception as e:
            logger.error(f"Error parsing file {file_path}: {e}")
            return []
    
    def parse_java_code(self, source_code: str, file_path: str) -> List[CodeChunk]:
        """Parse Java source code and extract semantic chunks."""
        try:
            tree = self.parser.parse(bytes(source_code, 'utf8'))
            chunks = []
            
            # Extract chunks from the syntax tree
            self._extract_chunks(tree.root_node, source_code, file_path, chunks)
            
            return chunks
            
        except Exception as e:
            logger.error(f"Error parsing Java code: {e}")
            return []
    
    def _extract_chunks(self, node, source_code: str, file_path: str, chunks: List[CodeChunk]):
        """Recursively extract code chunks from the syntax tree."""
        lines = source_code.split('\n')
        
        # Handle different node types
        if node.type == 'method_declaration':
            chunk = self._create_method_chunk(node, source_code, file_path, lines)
            if chunk:
                chunks.append(chunk)
        
        elif node.type == 'class_declaration':
            chunk = self._create_class_chunk(node, source_code, file_path, lines)
            if chunk:
                chunks.append(chunk)
        
        elif node.type == 'interface_declaration':
            chunk = self._create_interface_chunk(node, source_code, file_path, lines)
            if chunk:
                chunks.append(chunk)
        
        elif node.type == 'field_declaration':
            chunk = self._create_field_chunk(node, source_code, file_path, lines)
            if chunk:
                chunks.append(chunk)
        
        # Recursively process child nodes
        for child in node.children:
            self._extract_chunks(child, source_code, file_path, chunks)
    
    def _create_method_chunk(self, node, source_code: str, file_path: str, lines: List[str]) -> Optional[CodeChunk]:
        """Create a code chunk for a method declaration."""
        try:
            start_line = node.start_point[0] + 1
            end_line = node.end_point[0] + 1
            
            # Extract method content
            content = self._get_node_text(node, source_code)
            
            # Extract method name
            method_name = self._find_method_name(node)
            
            # Find the containing class
            class_name = self._find_containing_class(node, source_code)
            
            # Extract additional metadata
            metadata = {
                'modifiers': self._extract_modifiers(node),
                'parameters': self._extract_parameters(node),
                'return_type': self._extract_return_type(node),
                'annotations': self._extract_annotations(node)
            }
            
            return CodeChunk(
                content=content,
                source_file=file_path,
                class_name=class_name,
                method_name=method_name,
                start_line=start_line,
                end_line=end_line,
                chunk_type='method',
                metadata=metadata
            )
        except Exception as e:
            logger.warning(f"Error creating method chunk: {e}")
            return None
    
    def _create_class_chunk(self, node, source_code: str, file_path: str, lines: List[str]) -> Optional[CodeChunk]:
        """Create a code chunk for a class declaration."""
        try:
            start_line = node.start_point[0] + 1
            end_line = node.end_point[0] + 1
            
            # Extract class content (just the declaration, not the full body)
            class_header = self._extract_class_header(node, source_code)
            
            class_name = self._find_class_name(node)
            
            metadata = {
                'modifiers': self._extract_modifiers(node),
                'extends': self._extract_extends(node),
                'implements': self._extract_implements(node),
                'annotations': self._extract_annotations(node)
            }
            
            return CodeChunk(
                content=class_header,
                source_file=file_path,
                class_name=class_name,
                method_name=None,
                start_line=start_line,
                end_line=start_line + 10,  # Just the header
                chunk_type='class',
                metadata=metadata
            )
        except Exception as e:
            logger.warning(f"Error creating class chunk: {e}")
            return None
    
    def _create_interface_chunk(self, node, source_code: str, file_path: str, lines: List[str]) -> Optional[CodeChunk]:
        """Create a code chunk for an interface declaration."""
        try:
            start_line = node.start_point[0] + 1
            end_line = node.end_point[0] + 1
            
            content = self._get_node_text(node, source_code)
            interface_name = self._find_interface_name(node)
            
            metadata = {
                'modifiers': self._extract_modifiers(node),
                'extends': self._extract_extends(node),
                'annotations': self._extract_annotations(node)
            }
            
            return CodeChunk(
                content=content,
                source_file=file_path,
                class_name=interface_name,
                method_name=None,
                start_line=start_line,
                end_line=end_line,
                chunk_type='interface',
                metadata=metadata
            )
        except Exception as e:
            logger.warning(f"Error creating interface chunk: {e}")
            return None
    
    def _create_field_chunk(self, node, source_code: str, file_path: str, lines: List[str]) -> Optional[CodeChunk]:
        """Create a code chunk for a field declaration."""
        try:
            start_line = node.start_point[0] + 1
            end_line = node.end_point[0] + 1
            
            content = self._get_node_text(node, source_code)
            field_name = self._find_field_name(node)
            class_name = self._find_containing_class(node, source_code)
            
            metadata = {
                'modifiers': self._extract_modifiers(node),
                'type': self._extract_field_type(node),
                'annotations': self._extract_annotations(node)
            }
            
            return CodeChunk(
                content=content,
                source_file=file_path,
                class_name=class_name,
                method_name=field_name,
                start_line=start_line,
                end_line=end_line,
                chunk_type='field',
                metadata=metadata
            )
        except Exception as e:
            logger.warning(f"Error creating field chunk: {e}")
            return None
    
    def _get_node_text(self, node, source_code: str) -> str:
        """Extract text content of a node."""
        return source_code[node.start_byte:node.end_byte]
    
    def _find_method_name(self, node) -> Optional[str]:
        """Find the method name from a method declaration node."""
        for child in node.children:
            if child.type == 'identifier':
                return child.text.decode('utf-8')
        return None
    
    def _find_class_name(self, node) -> Optional[str]:
        """Find the class name from a class declaration node."""
        for child in node.children:
            if child.type == 'identifier':
                return child.text.decode('utf-8')
        return None
    
    def _find_interface_name(self, node) -> Optional[str]:
        """Find the interface name from an interface declaration node."""
        for child in node.children:
            if child.type == 'identifier':
                return child.text.decode('utf-8')
        return None
    
    def _find_field_name(self, node) -> Optional[str]:
        """Find the field name from a field declaration node."""
        for child in node.children:
            if child.type == 'variable_declarator':
                for grandchild in child.children:
                    if grandchild.type == 'identifier':
                        return grandchild.text.decode('utf-8')
        return None
    
    def _find_containing_class(self, node, source_code: str) -> Optional[str]:
        """Find the containing class name for a given node."""
        current = node.parent
        while current:
            if current.type == 'class_declaration':
                return self._find_class_name(current)
            current = current.parent
        return None
    
    def _extract_class_header(self, node, source_code: str) -> str:
        """Extract just the class header (declaration line)."""
        lines = source_code.split('\n')
        start_line = node.start_point[0]
        
        # Find the opening brace
        for i, child in enumerate(node.children):
            if child.type == 'class_body':
                end_line = child.start_point[0]
                return '\n'.join(lines[start_line:end_line]).strip()
        
        return lines[start_line].strip()
    
    def _extract_modifiers(self, node) -> List[str]:
        """Extract modifiers (public, private, static, etc.)."""
        modifiers = []
        for child in node.children:
            if child.type == 'modifiers':
                for modifier in child.children:
                    if modifier.type in ['public', 'private', 'protected', 'static', 'final', 'abstract']:
                        modifiers.append(modifier.type)
        return modifiers
    
    def _extract_parameters(self, node) -> List[str]:
        """Extract method parameters."""
        parameters = []
        for child in node.children:
            if child.type == 'formal_parameters':
                for param in child.children:
                    if param.type == 'formal_parameter':
                        param_text = param.text.decode('utf-8')
                        parameters.append(param_text)
        return parameters
    
    def _extract_return_type(self, node) -> Optional[str]:
        """Extract method return type."""
        for child in node.children:
            if child.type in ['type_identifier', 'generic_type', 'array_type', 'void_type']:
                return child.text.decode('utf-8')
        return None
    
    def _extract_annotations(self, node) -> List[str]:
        """Extract annotations."""
        annotations = []
        for child in node.children:
            if child.type == 'annotation':
                annotations.append(child.text.decode('utf-8'))
        return annotations
    
    def _extract_extends(self, node) -> Optional[str]:
        """Extract extends clause."""
        for child in node.children:
            if child.type == 'superclass':
                return child.text.decode('utf-8')
        return None
    
    def _extract_implements(self, node) -> List[str]:
        """Extract implements clause."""
        implements = []
        for child in node.children:
            if child.type == 'super_interfaces':
                for interface in child.children:
                    if interface.type == 'type_identifier':
                        implements.append(interface.text.decode('utf-8'))
        return implements
    
    def _extract_field_type(self, node) -> Optional[str]:
        """Extract field type."""
        for child in node.children:
            if child.type in ['type_identifier', 'generic_type', 'array_type']:
                return child.text.decode('utf-8')
        return None