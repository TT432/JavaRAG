#!/usr/bin/env python3
"""
WebUI服务器 - 为JavaRAG提供Web界面
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Any

from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

# 导入项目模块
from ..config import settings
from ..rag_service import RAGService
from ..ingestion_pipeline import IngestionPipeline

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 请求模型
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]] = []

class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]

class StatusResponse(BaseModel):
    status: str
    message: str = ""

class StatsResponse(BaseModel):
    indexed_files: int
    total_chunks: int
    database_size: str

# 创建FastAPI应用
app = FastAPI(
    title="JavaRAG WebUI",
    description="Java代码知识库RAG系统Web界面",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局变量
rag_service = None
ingestion_pipeline = None

# 获取前端文件路径
FRONTEND_DIR = Path(__file__).parent
STATIC_DIR = FRONTEND_DIR / "static"

# 挂载静态文件
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化服务"""
    global rag_service, ingestion_pipeline
    
    try:
        logger.info("初始化RAG服务...")
        rag_service = RAGService()
        
        logger.info("初始化数据摄取管道...")
        ingestion_pipeline = IngestionPipeline()
        
        logger.info("WebUI服务启动完成")
    except Exception as e:
        logger.error(f"服务初始化失败: {e}")
        raise

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """返回主页面"""
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return index_file.read_text(encoding='utf-8')
    else:
        raise HTTPException(status_code=404, detail="页面未找到")

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """上传JAR文件并进行索引"""
    if not file.filename.lower().endswith('.jar'):
        raise HTTPException(status_code=400, detail="只支持JAR文件")
    
    try:
        # 保存上传的文件
        upload_dir = settings.sources_dir
        upload_dir.mkdir(exist_ok=True)
        
        file_path = upload_dir / file.filename
        
        # 写入文件
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        logger.info(f"文件已保存: {file_path}")
        
        # 处理文件
        if ingestion_pipeline:
            await process_jar_file(str(file_path))
        
        return JSONResponse({
            "message": "文件上传并处理成功",
            "filename": file.filename,
            "size": len(content)
        })
        
    except Exception as e:
        logger.error(f"文件上传失败: {e}")
        raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")

async def process_jar_file(file_path: str):
    """异步处理JAR文件"""
    try:
        logger.info(f"开始处理JAR文件: {file_path}")
        
        # 使用数据摄取管道处理文件
        result = ingestion_pipeline.ingest_jar_file(Path(file_path))
        
        if result["success"]:
            logger.info(f"JAR文件处理完成: {file_path}, 处理了 {result['chunks_processed']} 个代码块")
        else:
            logger.error(f"JAR文件处理失败: {result['error']}")
            raise Exception(result["error"])
        
    except Exception as e:
        logger.error(f"JAR文件处理失败: {e}")
        raise

@app.post("/api/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    """查询知识库"""
    if not rag_service:
        raise HTTPException(status_code=503, detail="RAG服务未初始化")
    
    try:
        logger.info(f"处理查询: {request.query}")
        
        result = rag_service.query(request.query)
        
        # 从RAG服务返回的字典中提取答案
        if isinstance(result, dict):
            answer = result.get("answer", "未找到相关答案")
            sources = result.get("retrieved_chunks", [])
        else:
            answer = str(result)
            sources = []
        
        return QueryResponse(
            answer=answer,
            sources=sources
        )
        
    except Exception as e:
        logger.error(f"查询失败: {e}")
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")

# Pydantic model for search POST request
class WebSearchRequest(BaseModel):
    query: str
    jar_filter: Optional[str] = None
    type_filter: Optional[str] = None
    top_k: int = 10

@app.post("/api/search", response_model=SearchResponse)
async def search_code_post(request: WebSearchRequest):
    """搜索代码片段 (POST)"""
    if not rag_service:
        raise HTTPException(status_code=503, detail="RAG服务未初始化")
    
    try:
        logger.info(f"搜索代码 (POST): query='{request.query}', jar_filter='{request.jar_filter}', type_filter='{request.type_filter}', top_k={request.top_k}")
        
        filters = {}
        if request.jar_filter:
            filters['jar_file'] = request.jar_filter
        if request.type_filter:
            filters['chunk_type'] = request.type_filter
        
        # Assuming rag_service has a method search_code that takes these params
        # and returns a list of dicts suitable for SearchResponse.
        # This aligns with how api_server.py uses rag_service.search_code.
        # If RAGService.search_code is not defined or has different signature, this might need adjustment
        # or use rag_service.vector_db.search and format results as before.
        # For now, let's assume rag_service.search_code is the preferred method.
        
        # Option 1: Use a direct method like in api_server.py if available and returns List[Dict]
        # search_results_list = rag_service.search_code(
        # query=request.query,
        # top_k=request.top_k,
        # filters=filters if filters else None
        # )

        # Option 2: Continue using vector_db.search and format, if search_code isn't suitable/available
        # This keeps the logic similar to the original GET endpoint but adapts to POST
        search_results_list = rag_service.vector_db.search(
            query=request.query,
            top_k=request.top_k,
            filters=filters if filters else None
        )

        # The search_results_list from vector_db.search is already a list of formatted dicts.
        # Each dict contains 'content', 'source_file', 'chunk_type', 'jar_file', etc.
        # We just need to pass this to SearchResponse, ensuring the keys match SearchResultItem.
        
        # Transform the list of dicts from vector_db.search to match SearchResultItem structure if necessary.
        # Based on vector_db.py, the keys should largely match.
        # SearchResultItem expects: content, source_file, chunk_type, jar_file
        # vector_db.search returns dicts with these keys among others.

        return SearchResponse(results=search_results_list)
    except Exception as e:
        logger.error(f"Error during search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status/database", response_model=StatusResponse)
async def check_database_status():
    """检查数据库状态"""
    try:
        if rag_service and rag_service.vector_db:
            # 尝试获取集合信息
            collection = rag_service.vector_db.collection
            count = collection.count()
            
            return StatusResponse(
                status="online",
                message=f"数据库在线，包含 {count} 个文档"
            )
        else:
            return StatusResponse(
                status="offline",
                message="数据库服务未初始化"
            )
    except Exception as e:
        logger.error(f"数据库状态检查失败: {e}")
        return StatusResponse(
            status="offline",
            message=f"数据库连接失败: {str(e)}"
        )

@app.get("/api/status/ai", response_model=StatusResponse)
async def check_ai_status():
    """检查AI服务状态"""
    try:
        if rag_service and rag_service.llm:
            # 尝试进行一个简单的测试查询
            test_response = rag_service.llm.invoke("test")
            
            return StatusResponse(
                status="online",
                message="AI服务在线"
            )
        else:
            return StatusResponse(
                status="offline",
                message="AI服务未初始化或API密钥未配置"
            )
    except Exception as e:
        logger.error(f"AI服务状态检查失败: {e}")
        return StatusResponse(
            status="offline",
            message=f"AI服务连接失败: {str(e)}"
        )

@app.delete("/api/jar/{jar_name}")
async def delete_jar(jar_name: str):
    """删除JAR文件及其索引数据"""
    try:
        # 删除文件系统中的JAR文件
        jar_path = settings.sources_dir / jar_name
        if jar_path.exists():
            jar_path.unlink()
            logger.info(f"已删除JAR文件: {jar_path}")
        
        # 从向量数据库中删除相关数据
        if rag_service and rag_service.vector_db:
            # 删除与该JAR文件相关的所有文档
            collection = rag_service.vector_db.collection
            # 根据jar_file元数据删除文档
            collection.delete(where={"jar_file": jar_name})
            logger.info(f"已从数据库删除JAR文件相关数据: {jar_name}")
        
        return JSONResponse({
            "message": f"JAR文件 {jar_name} 删除成功",
            "jar_name": jar_name
        })
        
    except Exception as e:
        logger.error(f"删除JAR文件失败: {e}")
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")

@app.get("/api/jars")
async def get_jar_files():
    """获取JAR文件列表"""
    try:
        jar_files = []
        sources_dir = settings.sources_dir
        
        if sources_dir.exists():
            for jar_file in sources_dir.glob("*.jar"):
                # 获取文件统计信息
                file_stats = jar_file.stat()
                upload_time = file_stats.st_mtime
                
                # 从向量数据库获取该JAR文件的块数量
                chunks = 0
                if rag_service and rag_service.vector_db:
                    try:
                        collection = rag_service.vector_db.collection
                        result = collection.get(where={"jar_file": jar_file.name})
                        chunks = len(result['ids']) if result['ids'] else 0
                    except Exception as e:
                        logger.warning(f"获取JAR文件块数量失败: {e}")
                
                jar_files.append({
                    "name": jar_file.name,
                    "status": "indexed" if chunks > 0 else "pending",
                    "chunks": chunks,
                    "uploadTime": upload_time,
                    "size": file_stats.st_size
                })
        
        return JSONResponse({"jars": jar_files})
        
    except Exception as e:
        logger.error(f"获取JAR文件列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取文件列表失败: {str(e)}")

@app.get("/api/stats", response_model=StatsResponse)
async def get_system_stats():
    """获取系统统计信息"""
    try:
        indexed_files = 0
        total_chunks = 0
        database_size = "0 MB"
        
        if rag_service and rag_service.vector_db:
            # 使用rag_service的统计方法获取准确信息
            stats = rag_service.get_stats()
            total_chunks = stats.get('total_chunks', 0)
            indexed_files = stats.get('unique_source_files', 0)
            
            # 估算数据库大小
            chroma_dir = Path(settings.chroma_persist_directory)
            if chroma_dir.exists():
                size_bytes = sum(f.stat().st_size for f in chroma_dir.rglob('*') if f.is_file())
                database_size = f"{size_bytes / (1024 * 1024):.1f} MB"
        
        return StatsResponse(
            indexed_files=indexed_files,
            total_chunks=total_chunks,
            database_size=database_size
        )
        
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        return StatsResponse(
            indexed_files=0,
            total_chunks=0,
            database_size="未知"
        )

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """404错误处理"""
    return JSONResponse(
        status_code=404,
        content={"detail": "页面或API端点未找到"}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    """500错误处理"""
    return JSONResponse(
        status_code=500,
        content={"detail": "服务器内部错误"}
    )

def run_webui_server(
    host: str = None,
    port: int = None,
    reload: bool = False
):
    """运行WebUI服务器"""
    # 使用配置文件中的设置或默认值
    host = host or getattr(settings, 'webui_host', '0.0.0.0')
    port = port or getattr(settings, 'webui_port', 8847)
    
    logger.info(f"启动WebUI服务器: http://{host}:{port}")
    
    uvicorn.run(
        "src.frontend.webui_server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    run_webui_server(reload=True)