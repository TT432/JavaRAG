#!/usr/bin/env python3
"""
WebUI启动脚本 - 启动JavaRAG Web界面
"""

import sys
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.frontend.webui_server import run_webui_server
from src.config import settings

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="JavaRAG WebUI服务器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用默认配置启动
  python webui.py
  
  # 指定端口启动
  python webui.py --port 9000
  
  # 开发模式启动（自动重载）
  python webui.py --reload
  
  # 指定主机和端口
  python webui.py --host 127.0.0.1 --port 8888
        """
    )
    
    parser.add_argument(
        "--host",
        default=settings.webui_host,
        help=f"服务器主机地址 (默认: {settings.webui_host})"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=settings.webui_port,
        help=f"服务器端口 (默认: {settings.webui_port})"
    )
    
    parser.add_argument(
        "--reload",
        action="store_true",
        help="开启自动重载模式（开发用）"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="显示详细日志"
    )
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    
    print(f"🚀 启动JavaRAG WebUI服务器...")
    print(f"📍 地址: http://{args.host}:{args.port}")
    print(f"🔧 配置文件: .env")
    print(f"📁 数据目录: {settings.chroma_persist_directory}")
    print("\n按 Ctrl+C 停止服务器\n")
    
    try:
        run_webui_server(
            host=args.host,
            port=args.port,
            reload=args.reload
        )
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()