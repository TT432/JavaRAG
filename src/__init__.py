#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JavaRAG - Java代码知识库RAG系统

这是一个基于检索增强生成(RAG)技术的Java代码知识库系统，
支持从JAR文件中提取Java代码，构建向量数据库，并提供智能问答功能。
"""

__version__ = "1.0.0"
__author__ = "JavaRAG Team"
__description__ = "Java代码知识库RAG系统"

# 导出主要类和函数
from .rag_service import RAGService
from .vector_db import VectorDatabase
from .java_parser import JavaParser, CodeChunk
from .jar_processor import JarProcessor
from .config import Settings

__all__ = [
    "RAGService",
    "VectorDatabase", 
    "JavaParser",
    "CodeChunk",
    "JarProcessor",
    "Settings"
]