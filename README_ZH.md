# JavaRAG - Java代码知识库系统

> **Language / 语言**: [English](README.md) | [中文](README_ZH.md)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![uv](https://img.shields.io/badge/uv-enabled-brightgreen.svg)](https://github.com/astral-sh/uv)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.4%2B-FF6B6B.svg)](https://www.trychroma.com/)

一个基于检索增强生成(RAG)技术的Java代码知识库系统，专门用于解析、索引和查询Java源代码。该系统能够从JAR文件中自动提取Java源代码，使用先进的向量化技术构建代码知识库，并通过集成硅基流动API和DeepSeek-V3模型提供智能的代码问答服务。

## 🎯 项目简介

### 解决的问题

JavaRAG旨在解决以下Java开发中的常见问题：

1. **代码理解困难**: 面对大型Java项目时，开发者难以快速理解复杂的代码结构和逻辑
2. **API文档不足**: 许多开源Java库缺乏详细的文档，开发者需要直接阅读源码
3. **代码搜索效率低**: 传统的文本搜索无法理解代码的语义，难以找到相关的代码片段
4. **知识传承困难**: 项目中的代码知识难以有效传承给新团队成员
5. **代码复用率低**: 开发者难以发现项目中已有的可复用代码组件

### 核心价值

- **智能代码理解**: 基于AI的代码语义理解，提供准确的代码解释和问答
- **高效知识检索**: 向量化搜索技术，快速定位相关代码片段
- **自动化处理**: 自动从JAR文件提取和解析Java源代码
- **多样化接口**: 提供CLI、Web UI和REST API多种使用方式
- **可扩展架构**: 模块化设计，易于扩展和定制

## ✨ 主要特性

- 🔍 **智能代码解析**: 自动解析JAR文件中的Java源代码
- 🧠 **向量化存储**: 使用ChromaDB构建高效的代码向量数据库
- 💬 **智能问答**: 基于RAG技术的Java代码问答系统
- 🚀 **硅基流动集成**: 集成DeepSeek-V3模型，提供强大的代码理解能力
- 🌐 **Web API**: 提供RESTful API接口
- 🖥️ **命令行工具**: 支持命令行操作
- 🎨 **Web界面**: 现代化的Web UI界面

## 📁 项目结构

```
javarag/
├── .AddCompLib/                 # AddCompLib 配置
├── .env                         # 环境变量配置
├── .env.example                 # 环境变量示例
├── .gitignore                   # Git忽略文件配置
├── .venv/                       # Python虚拟环境
├── README.md                    # 项目自述文件
├── TODO.md                      # TODO列表
├── chroma_db/                   # ChromaDB数据目录
├── pyproject.toml               # 项目配置 (PEP 518)
├── src/                         # 核心源代码
│   ├── __init__.py              # 包初始化文件
│   ├── config.py                # 配置管理
│   ├── demo.py                  # 演示脚本
│   ├── frontend/                # Web前端界面
│   │   ├── index.html           # 主页面
│   │   ├── webui_server.py      # WebUI服务器
│   │   └── static/              # 静态资源 (CSS, JS等)
│   ├── ingestion_pipeline.py    # 数据摄取管道
│   ├── jar_processor.py         # JAR文件处理器
│   ├── java_parser.py           # Java代码解析器
│   ├── rag_service.py           # RAG服务核心
│   ├── sources/                 # JAR文件存储目录
│   ├── temp/                    # 临时文件目录
│   └── vector_db.py             # 向量数据库操作
├── uv.lock                      # uv依赖锁定文件
└── webui.py                     # WebUI启动脚本
```

## 🚀 快速开始

### 环境要求

- **Python**: 3.10+ (推荐使用3.11或3.12)
- **包管理器**: uv (推荐) 或 pip
- **API密钥**: 硅基流动API密钥 (用于AI问答功能)
- **系统要求**: 
  - 内存: 最少4GB RAM (推荐8GB+)
  - 存储: 至少2GB可用空间
  - 网络: 稳定的互联网连接 (用于下载模型和API调用)

### 安装步骤

#### 方法一: 使用uv (推荐)

[uv](https://github.com/astral-sh/uv) 是一个快速的Python包管理器，能够显著提升依赖安装速度。

```bash
# 1. 安装uv (如果尚未安装)
curl -LsSf https://astral.sh/uv/install.sh | sh  # Linux/Mac
# 或在Windows上使用PowerShell:
# powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. 克隆项目
git clone <repository-url>
cd javarag

# 3. 创建虚拟环境并安装依赖
uv sync

# 4. 激活虚拟环境
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows
```

#### 方法二: 使用pip

```bash
# 1. 克隆项目
git clone <repository-url>
cd javarag

# 2. 创建虚拟环境
python -m venv .venv

# 3. 激活虚拟环境
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows

# 4. 升级pip并安装依赖
pip install --upgrade pip
pip install .
```

### 配置

1. 复制环境变量示例文件：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，配置硅基流动API：
```env
# 硅基流动API配置
OPENAI_API_KEY=your_siliconflow_api_key
OPENAI_API_BASE=https://api.siliconflow.cn/v1
OPENAI_MODEL=deepseek-ai/DeepSeek-V3

# ChromaDB配置
CHROMA_PERSIST_DIRECTORY=./chroma_db

# API服务器配置
API_HOST=0.0.0.0
API_PORT=8000

# WebUI配置
WEBUI_HOST=0.0.0.0
WEBUI_PORT=8847

# LLM配置
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=1000

# 嵌入模型配置
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### 数据摄取

将JAR文件放入 `src/sources/` 目录，然后运行数据摄取管道：

```bash
# 使用uv
uv run python src/ingestion_pipeline.py --jar-path src/sources

# 使用python
python src/ingestion_pipeline.py --jar-path src/sources
```

## 📖 使用方式

### Web用户界面 (WebUI)

#### 启动WebUI服务器

```bash
# 使用默认配置启动
python webui.py

# 指定端口和主机
python webui.py --host 0.0.0.0 --port 9000

# 开发模式启动（自动重载）
python webui.py --reload

# 使用uv运行
uv run python webui.py --verbose
```

#### WebUI功能特性

访问 `http://localhost:8847` 后，您可以使用以下功能：

- **📁 文件管理**:
  - 拖拽上传JAR文件
  - 查看已索引的文件列表
  - 删除不需要的文件
  - 重新索引文件

- **💬 智能问答**:
  - 自然语言查询Java代码
  - 查看AI生成的详细回答
  - 查看相关的源代码片段
  - 复制代码到剪贴板

- **🔍 代码搜索**:
  - 语义搜索代码片段
  - 精确匹配类名和方法名
  - 按文件类型过滤结果
  - 高亮显示匹配内容

### Python编程接口

#### 基本使用

```python
from src.rag_service import RAGService
from src.vector_db import VectorDatabase
from src.ingestion_pipeline import IngestionPipeline

# 初始化RAG服务
rag = RAGService(collection_name="java_code_chunks")

# 查询代码
result = rag.query(
    query="什么是Spring Boot的自动配置？",
    top_k=5,
    include_sources=True
)

print(f"回答: {result['answer']}")
print(f"相关源码: {len(result['sources'])} 个片段")
```

#### 高级使用

```python
# 自定义配置
from src.config import settings

# 修改配置
settings.llm_temperature = 0.2
settings.llm_max_tokens = 2000

# 初始化数据摄取管道
pipeline = IngestionPipeline()

# 处理JAR文件
result = pipeline.ingest_jar_file(
    jar_path="path/to/your-sources.jar",
    reset_collection=False
)

if result["success"]:
    print(f"成功处理 {result['chunks_processed']} 个代码块")
else:
    print(f"处理失败: {result['error']}")

# 直接操作向量数据库
vector_db = VectorDatabase("custom_collection")

# 搜索相似代码
similar_chunks = vector_db.search(
    query="dependency injection",
    top_k=10,
    filter_metadata={"file_type": "java"}
)

for chunk in similar_chunks:
    print(f"文件: {chunk['source_file']}")
    print(f"相似度: {chunk['similarity']:.3f}")
    print(f"代码: {chunk['content'][:200]}...")
    print("-" * 50)
```

## 🛠️ 技术栈与依赖库

### 核心技术栈

| 技术组件 | 版本要求 | 用途说明 |
|---------|---------|----------|
| **Python** | 3.10+ | 主要编程语言 |
| **FastAPI** | 0.104+ | Web API框架，提供高性能的REST API服务 |
| **Uvicorn** | 0.24+ | ASGI服务器，用于运行FastAPI应用 |
| **ChromaDB** | 0.4.22+ | 向量数据库，存储和检索代码嵌入向量 |
| **LangChain** | 0.1.0+ | LLM应用开发框架，提供RAG功能 |
| **Sentence Transformers** | 2.2.2+ | 文本嵌入模型，将代码转换为向量 |
| **Tree-sitter** | 0.20.4+ | 代码解析器，用于解析Java语法树 |

### AI和机器学习库

| 库名称 | 版本 | 功能描述 |
|-------|------|----------|
| **langchain-openai** | 0.0.5+ | OpenAI兼容的LLM接口 |
| **langchain-community** | 0.0.20+ | LangChain社区扩展 |
| **sentence-transformers** | 2.2.2+ | 预训练的句子嵌入模型 |
| **numpy** | 1.24.0+ | 数值计算库 |
| **pandas** | 2.0.0+ | 数据处理和分析 |

### Web开发和API库

| 库名称 | 版本 | 功能描述 |
|-------|------|----------|
| **fastapi** | 0.104.1+ | 现代化的Web API框架 |
| **uvicorn** | 0.24.0+ | 高性能ASGI服务器 |
| **python-multipart** | 0.0.6+ | 文件上传支持 |
| **aiofiles** | 23.2.1+ | 异步文件操作 |
| **httpx** | 0.25.0+ | 异步HTTP客户端 |

### 配置和工具库

| 库名称 | 版本 | 功能描述 |
|-------|------|----------|
| **pydantic** | 2.5.0+ | 数据验证和设置管理 |
| **pydantic-settings** | 2.1.0+ | 配置管理 |
| **python-dotenv** | 1.0.0+ | 环境变量管理 |
| **click** | 8.1.7+ | 命令行界面框架 |
| **rich** | 13.7.0+ | 终端美化和进度条 |
| **tqdm** | 4.66.1+ | 进度条显示 |

### 开发和测试工具

| 库名称 | 版本 | 功能描述 |
|-------|------|----------|
| **pytest** | 7.4.0+ | 单元测试框架 |
| **pytest-asyncio** | 0.21.0+ | 异步测试支持 |
| **black** | 23.0.0+ | 代码格式化工具 |
| **flake8** | 6.0.0+ | 代码风格检查 |
| **mypy** | 1.5.0+ | 静态类型检查 |

## 🗄️ 数据库架构

### ChromaDB向量数据库

JavaRAG使用ChromaDB作为向量数据库，用于存储和检索Java代码的嵌入向量。

#### 数据库配置

```python
# 数据库设置
CHROMA_PERSIST_DIRECTORY = "./chroma_db"  # 数据持久化目录
COLLECTION_NAME = "java_code_chunks"     # 默认集合名称
EMBEDDING_MODEL = "all-MiniLM-L6-v2"    # 嵌入模型
```

#### 数据结构

每个代码块在数据库中存储以下信息：

```python
{
    "id": "unique_chunk_id",           # 唯一标识符
    "content": "Java代码内容",          # 代码文本
    "embedding": [0.1, 0.2, ...],      # 384维向量
    "metadata": {
        "source_file": "com/example/MyClass.java",
        "class_name": "MyClass",
        "method_name": "myMethod",
        "start_line": 10,
        "end_line": 25,
        "chunk_type": "method",        # method, class, interface, field
        "file_type": "java",
        "jar_source": "spring-core-6.0.0-sources.jar",
        "package_name": "com.example",
        "access_modifier": "public",
        "is_static": false,
        "is_abstract": false,
        "annotations": ["@Override", "@Deprecated"]
    }
}
```

#### 索引策略

1. **语义索引**: 使用sentence-transformers模型生成代码的语义嵌入
2. **元数据索引**: 基于类名、方法名、包名等元数据进行过滤
3. **混合检索**: 结合语义相似性和元数据匹配

#### 查询优化

```python
# 查询示例
similar_chunks = vector_db.search(
    query="Spring dependency injection",
    top_k=10,
    filter_metadata={
        "chunk_type": "method",
        "package_name": "org.springframework"
    },
    similarity_threshold=0.7
)
```

### 数据持久化

- **存储位置**: `./chroma_db/` 目录
- **备份策略**: 支持数据库导出和导入
- **版本控制**: 支持集合版本管理
- **数据迁移**: 提供数据迁移工具

## 🧪 测试

### 测试框架

项目使用pytest作为主要测试框架，支持单元测试、集成测试和端到端测试。

### 运行测试

#### 单元测试
```bash
# 运行所有单元测试
uv run pytest tests/ -v

# 运行特定测试文件
uv run pytest tests/test_vector_db.py -v

# 运行带覆盖率的测试
uv run pytest tests/ --cov=src --cov-report=html
```

#### 集成测试
```bash
# 测试硅基流动API连接
uv run python tests_integration/test_siliconflow.py

# 系统集成测试
uv run python tests_integration/test_system.py

# 端到端测试
uv run pytest tests_integration/ -v
```

#### 性能测试
```bash
# 向量数据库性能测试
uv run python tests/test_performance.py

# API响应时间测试
uv run python tests_integration/test_api_performance.py
```

### 测试覆盖率

目标测试覆盖率：
- 核心模块: >90%
- API接口: >85%
- 工具函数: >80%

## 🐳 Docker部署

### 使用Docker Compose (推荐)

```bash
# 构建并启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 使用Docker

```bash
# 构建镜像
docker build -t javarag .

# 运行容器
docker run -d -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key \
  -e OPENAI_BASE_URL=https://api.siliconflow.cn/v1 \
  -v $(pwd)/sources:/app/sources \
  -v $(pwd)/chroma_db:/app/chroma_db \
  javarag
```

## 📚 API文档

启动API服务器后，访问以下地址查看API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 主要API端点

- `POST /query` - 查询Java代码
- `GET /health` - 健康检查
- `GET /stats` - 系统统计信息

## ⚙️ 配置说明

### 环境变量

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `OPENAI_API_KEY` | 硅基流动API密钥 | 必填 |
| `OPENAI_BASE_URL` | API基础URL | `https://api.siliconflow.cn/v1` |
| `OPENAI_MODEL` | 使用的模型 | `deepseek-ai/DeepSeek-V3` |
| `CHROMA_DB_PATH` | ChromaDB数据路径 | `./chroma_db` |
| `COLLECTION_NAME` | 集合名称 | `java_code_chunks` |
| `CHUNK_SIZE` | 代码块大小 | `1000` |
| `CHUNK_OVERLAP` | 代码块重叠 | `200` |
| `TOP_K` | 检索结果数量 | `5` |

### 支持的模型

硅基流动平台支持多种开源模型：
- DeepSeek系列：`deepseek-ai/DeepSeek-V3`、`deepseek-ai/DeepSeek-R1`
- Qwen系列：`Qwen/Qwen2.5-72B-Instruct`、`Qwen/Qwen2.5-Coder-32B-Instruct`
- GLM系列：`THUDM/glm-4-9b-chat`

## 🔧 开发指南

## 🏗️ 项目架构

### 系统架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户接口层 (User Interface Layer)          │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   命令行界面     │    Web用户界面   │       REST API接口           │
│   (CLI)         │    (WebUI)      │       (FastAPI)             │
│   cli.py        │   webui.py      │      api_server.py          │
└─────────────────┴─────────────────┴─────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                       业务逻辑层 (Business Logic Layer)           │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   RAG服务       │   数据摄取管道   │       配置管理               │
│   (RAG Service) │  (Ingestion)    │      (Configuration)        │
│  rag_service.py │ ingestion_*.py  │      config.py              │
└─────────────────┴─────────────────┴─────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                       数据处理层 (Data Processing Layer)          │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   Java解析器    │   JAR处理器     │       向量数据库             │
│  (Java Parser)  │ (JAR Processor) │    (Vector Database)        │
│  java_parser.py │jar_processor.py │     vector_db.py            │
└─────────────────┴─────────────────┴─────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                       外部服务层 (External Services Layer)        │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   硅基流动API   │    ChromaDB     │      Sentence Transformers  │
│  (SiliconFlow)  │   (Vector DB)   │      (Embedding Model)      │
│   DeepSeek-V3   │   持久化存储     │       文本向量化             │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

### 核心组件详解

#### 1. 用户接口层 (User Interface Layer)

**命令行界面 (CLI)**
- **文件**: `cli.py`
- **功能**: 提供命令行操作接口
- **主要命令**:
  - `ingest`: 数据摄取和索引
  - `query`: 代码查询和问答
  - `interactive`: 交互式问答模式
  - `status`: 系统状态检查

**Web用户界面 (WebUI)**
- **文件**: `webui.py`, `src/frontend/`
- **技术**: FastAPI + HTML/CSS/JavaScript
- **功能**: 图形化操作界面
- **特性**: 文件上传、实时问答、代码搜索、系统监控

**REST API接口**
- **文件**: `api_server.py`
- **技术**: FastAPI + Uvicorn
- **端点**: `/api/query`, `/api/search`, `/api/upload`, `/api/stats`
- **文档**: 自动生成Swagger/OpenAPI文档

#### 2. 业务逻辑层 (Business Logic Layer)

**RAG服务 (RAGService)**
- **文件**: `src/rag_service.py`
- **职责**: 核心RAG逻辑实现
- **功能**:
  - 查询处理和上下文检索
  - LLM调用和响应生成
  - 结果后处理和格式化

**数据摄取管道 (IngestionPipeline)**
- **文件**: `src/ingestion_pipeline.py`
- **职责**: 数据处理流水线
- **流程**:
  1. JAR文件验证和解压
  2. Java源码解析和分块
  3. 向量化和数据库存储
  4. 索引构建和优化

**配置管理 (Configuration)**
- **文件**: `src/config.py`
- **技术**: Pydantic Settings
- **功能**: 环境变量管理、配置验证、默认值设置

#### 3. 数据处理层 (Data Processing Layer)

**Java解析器 (JavaParser)**
- **文件**: `src/java_parser.py`
- **技术**: Tree-sitter
- **功能**:
  - Java语法树解析
  - 代码结构分析 (类、方法、字段)
  - 语义信息提取
  - 代码块分割和标注

**JAR处理器 (JarProcessor)**
- **文件**: `src/jar_processor.py`
- **功能**:
  - JAR文件解压和验证
  - 源码文件过滤和提取
  - 批量处理和错误处理
  - 临时文件管理

**向量数据库 (VectorDatabase)**
- **文件**: `src/vector_db.py`
- **技术**: ChromaDB + Sentence Transformers
- **功能**:
  - 代码向量化和存储
  - 语义相似性搜索
  - 元数据过滤和排序
  - 数据库管理和维护

#### 4. 外部服务层 (External Services Layer)

**硅基流动API**
- **模型**: DeepSeek-V3
- **用途**: 代码理解和问答生成
- **特性**: 高质量代码解释、多语言支持

**ChromaDB**
- **类型**: 向量数据库
- **用途**: 代码嵌入存储和检索
- **特性**: 持久化存储、高效查询、元数据过滤

**Sentence Transformers**
- **模型**: all-MiniLM-L6-v2
- **用途**: 文本向量化
- **特性**: 多语言支持、高质量嵌入

### 数据流图

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   JAR文件   │───▶│  解压提取   │───▶│  Java源码   │
└─────────────┘    └─────────────┘    └─────────────┘
                                              │
                                              ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  代码向量   │◀───│  向量化处理  │◀───│  语法解析   │
└─────────────┘    └─────────────┘    └─────────────┘
       │
       ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ ChromaDB存储│───▶│  相似性搜索  │───▶│  上下文检索  │
└─────────────┘    └─────────────┘    └─────────────┘
                                              │
                                              ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  最终答案   │◀───│   LLM生成   │◀───│  提示构建   │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 模块依赖关系

```
config.py
    ↑
    │
rag_service.py ←→ vector_db.py
    ↑                 ↑
    │                 │
ingestion_pipeline.py
    ↑                 ↑
    │                 │
jar_processor.py → java_parser.py
    ↑
    │
cli.py / webui.py / api_server.py
```

## 📚 详细技术文档

### API接口文档

#### REST API端点

**基础信息**
- 基础URL: `http://localhost:8000`
- 内容类型: `application/json`
- 认证: 无需认证 (可根据需要添加)

**健康检查**
```http
GET /health
```

响应:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "version": "1.0.0"
}
```

**代码查询**
```http
POST /api/query
Content-Type: application/json

{
  "query": "如何在Spring中配置数据源？",
  "top_k": 5,
  "include_sources": true,
  "temperature": 0.1,
  "max_tokens": 1000
}
```

响应:
```json
{
  "answer": "在Spring中配置数据源的方法有多种...",
  "sources": [
    {
      "content": "@Configuration\npublic class DataSourceConfig {...}",
      "source_file": "com/example/config/DataSourceConfig.java",
      "class_name": "DataSourceConfig",
      "method_name": null,
      "similarity": 0.95,
      "start_line": 10,
      "end_line": 30
    }
  ],
  "query_time": 1.23,
  "total_chunks": 150
}
```

**代码搜索**
```http
POST /api/search
Content-Type: application/json

{
  "query": "@Configuration",
  "limit": 10,
  "filter": {
    "chunk_type": "class",
    "package_name": "com.example"
  },
  "similarity_threshold": 0.7
}
```

**文件上传**
```http
POST /api/upload
Content-Type: multipart/form-data

file: [JAR文件]
reset_collection: false
```

**系统统计**
```http
GET /api/stats
```

响应:
```json
{
  "indexed_files": 25,
  "total_chunks": 1500,
  "database_size": "45.2 MB",
  "collections": ["java_code_chunks"],
  "embedding_model": "all-MiniLM-L6-v2",
  "last_update": "2024-01-01T12:00:00Z"
}
```

### 核心类和方法文档

#### RAGService类

```python
class RAGService:
    """RAG服务核心类，提供代码查询和问答功能。"""
    
    def __init__(self, collection_name: str = "java_code_chunks"):
        """初始化RAG服务。
        
        Args:
            collection_name: ChromaDB集合名称
        """
    
    def query(self, 
             query: str, 
             top_k: int = 5, 
             include_sources: bool = True,
             filter_metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """查询Java代码并生成回答。
        
        Args:
            query: 用户查询问题
            top_k: 返回的相关代码块数量
            include_sources: 是否包含源代码信息
            filter_metadata: 元数据过滤条件
            
        Returns:
            包含答案和源代码的字典
        """
    
    def search_similar_code(self, 
                           query: str, 
                           top_k: int = 10) -> List[Dict[str, Any]]:
        """搜索相似的代码片段。
        
        Args:
            query: 搜索查询
            top_k: 返回结果数量
            
        Returns:
            相似代码片段列表
        """
```

#### VectorDatabase类

```python
class VectorDatabase:
    """向量数据库管理类。"""
    
    def add_chunks(self, chunks: List[CodeChunk]) -> None:
        """添加代码块到向量数据库。
        
        Args:
            chunks: 代码块列表
        """
    
    def search(self, 
              query: str, 
              top_k: int = 10,
              filter_metadata: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """搜索相似的代码块。
        
        Args:
            query: 搜索查询
            top_k: 返回结果数量
            filter_metadata: 元数据过滤条件
            
        Returns:
            搜索结果列表
        """
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """获取集合统计信息。
        
        Returns:
            统计信息字典
        """
```

#### JavaParser类

```python
class JavaParser:
    """Java代码解析器。"""
    
    def parse_file(self, file_path: Path) -> List[CodeChunk]:
        """解析Java文件并提取代码块。
        
        Args:
            file_path: Java文件路径
            
        Returns:
            代码块列表
        """
    
    def extract_methods(self, source_code: str) -> List[Dict[str, Any]]:
        """提取Java代码中的方法。
        
        Args:
            source_code: Java源代码
            
        Returns:
            方法信息列表
        """
```

### 配置参数详解

#### 环境变量配置

```bash
# AI模型配置
OPENAI_API_KEY=sk-xxx                    # 硅基流动API密钥 (必填)
OPENAI_API_BASE=https://api.siliconflow.cn/v1  # API基础URL
OPENAI_MODEL=deepseek-ai/DeepSeek-V3     # 使用的模型

# 数据库配置
CHROMA_PERSIST_DIRECTORY=./chroma_db     # ChromaDB数据目录
EMBEDDING_MODEL=all-MiniLM-L6-v2        # 嵌入模型

# 服务器配置
API_HOST=0.0.0.0                        # API服务器主机
API_PORT=8000                           # API服务器端口
WEBUI_HOST=0.0.0.0                      # WebUI服务器主机
WEBUI_PORT=8847                         # WebUI服务器端口

# LLM参数配置
LLM_TEMPERATURE=0.1                     # 生成温度 (0.0-2.0)
LLM_MAX_TOKENS=1000                     # 最大生成token数

# 代码处理配置
CHUNK_SIZE=1000                         # 代码块大小
CHUNK_OVERLAP=200                       # 代码块重叠
TOP_K=5                                 # 默认检索结果数
```

#### 高级配置选项

```python
# src/config.py 中的高级配置
class AdvancedSettings:
    # 向量搜索配置
    similarity_threshold: float = 0.7    # 相似度阈值
    max_search_results: int = 100        # 最大搜索结果数
    
    # 代码解析配置
    supported_file_extensions = [".java"]  # 支持的文件扩展名
    ignore_patterns = ["test", "Test"]     # 忽略的文件模式
    
    # 性能配置
    batch_size: int = 50                 # 批处理大小
    max_workers: int = 4                 # 最大工作线程数
    cache_size: int = 1000               # 缓存大小
    
    # 日志配置
    log_level: str = "INFO"              # 日志级别
    log_format: str = "%(asctime)s - %(levelname)s - %(message)s"
```

### 性能优化指南

#### 1. 向量数据库优化

```python
# 批量插入优化
def batch_insert_chunks(chunks: List[CodeChunk], batch_size: int = 100):
    """批量插入代码块以提高性能。"""
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        vector_db.add_chunks(batch)

# 索引优化
vector_db.create_index(
    metric="cosine",           # 相似度计算方法
    n_trees=10,               # 索引树数量
    search_k=-1               # 搜索参数
)
```

#### 2. 内存管理

```python
# 大文件处理优化
def process_large_jar(jar_path: Path):
    """处理大型JAR文件的内存优化策略。"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # 分批处理文件
        for java_file in extract_java_files(jar_path):
            chunks = parser.parse_file(java_file)
            vector_db.add_chunks(chunks)
            # 及时清理内存
            del chunks
            gc.collect()
```

#### 3. 并发处理

```python
from concurrent.futures import ThreadPoolExecutor

def parallel_processing(jar_files: List[Path]):
    """并行处理多个JAR文件。"""
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_jar_file, jar) 
                  for jar in jar_files]
        
        for future in futures:
            result = future.result()
            print(f"处理完成: {result}")
```

### 错误处理和调试

#### 常见错误及解决方案

**1. API密钥错误**
```
Error: OpenAI API key not found
解决方案: 检查.env文件中的OPENAI_API_KEY配置
```

**2. ChromaDB连接失败**
```
Error: Could not connect to ChromaDB
解决方案: 检查CHROMA_PERSIST_DIRECTORY路径权限
```

**3. 内存不足**
```
Error: Out of memory during processing
解决方案: 减少batch_size或增加系统内存
```

#### 调试模式

```bash
# 启用详细日志
export LOG_LEVEL=DEBUG
uv run python cli.py query "test" --verbose

# 性能分析
uv run python -m cProfile -o profile.stats cli.py query "test"
```

### 扩展开发指南

#### 添加新的代码解析器

```python
class PythonParser(BaseParser):
    """Python代码解析器示例。"""
    
    def __init__(self):
        # 初始化Python语法解析器
        pass
    
    def parse_file(self, file_path: Path) -> List[CodeChunk]:
        # 实现Python代码解析逻辑
        pass
```

#### 添加新的向量化模型

```python
class CustomEmbeddingModel:
    """自定义嵌入模型。"""
    
    def encode(self, texts: List[str]) -> np.ndarray:
        # 实现自定义向量化逻辑
        pass
```

#### 添加新的LLM提供商

```python
class CustomLLMProvider:
    """自定义LLM提供商。"""
    
    def generate_response(self, prompt: str) -> str:
        # 实现自定义LLM调用逻辑
        pass
```

### 代码规范和最佳实践

#### 代码风格

- **格式化**: 使用 `black` 进行代码格式化
- **导入排序**: 使用 `isort` 排序导入语句
- **类型检查**: 使用 `mypy` 进行静态类型检查
- **代码检查**: 使用 `flake8` 进行代码风格检查

```bash
# 代码格式化
uv run black src/ tests/

# 导入排序
uv run isort src/ tests/

# 类型检查
uv run mypy src/

# 代码检查
uv run flake8 src/ tests/
```

#### 测试规范

```python
# 测试文件命名: test_*.py
# 测试类命名: Test*
# 测试方法命名: test_*

class TestRAGService:
    """RAG服务测试类。"""
    
    def test_query_with_valid_input(self):
        """测试有效输入的查询功能。"""
        rag = RAGService()
        result = rag.query("test query")
        assert "answer" in result
        assert isinstance(result["sources"], list)
```

#### 文档规范

```python
def complex_function(param1: str, param2: int = 10) -> Dict[str, Any]:
    """复杂函数的文档示例。
    
    这个函数演示了如何编写标准的文档字符串。
    
    Args:
        param1: 第一个参数的描述
        param2: 第二个参数的描述，默认值为10
        
    Returns:
        包含结果的字典，格式如下:
        {
            "status": "success",
            "data": [...]
        }
        
    Raises:
        ValueError: 当param1为空时抛出
        TypeError: 当param2不是整数时抛出
        
    Example:
        >>> result = complex_function("test", 20)
        >>> print(result["status"])
        success
    """
    pass
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [硅基流动](https://siliconflow.cn/) - 提供强大的AI模型API
- [ChromaDB](https://www.trychroma.com/) - 向量数据库
- [LangChain](https://langchain.com/) - LLM应用开发框架
- [FastAPI](https://fastapi.tiangolo.com/) - 现代Web框架
- [uv](https://github.com/astral-sh/uv) - 快速Python包管理器

---

**JavaRAG** - 让Java代码知识触手可及 🚀