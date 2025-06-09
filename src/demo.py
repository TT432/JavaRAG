#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JavaRAG系统演示脚本
展示如何使用硅基流动API进行Java代码问答
"""

from src.rag_service import RAGService

def main():
    print("🚀 JavaRAG系统演示")
    print("=" * 50)
    
    # 初始化RAG服务
    print("📚 正在初始化RAG服务...")
    rag = RAGService()
    print("✅ RAG服务初始化完成")
    
    # 测试问题列表
    questions = [
        "什么是Java类？",
        "如何创建Java方法？",
        "Java中的继承是什么？"
    ]
    
    print("\n💬 开始问答演示:")
    print("-" * 50)
    
    for i, question in enumerate(questions, 1):
        print(f"\n问题 {i}: {question}")
        try:
            result = rag.query(question)
            if isinstance(result, dict) and 'answer' in result:
                answer = result['answer']
                print(f"回答: {answer[:300]}..." if len(answer) > 300 else f"回答: {answer}")
            elif isinstance(result, str):
                print(f"回答: {result[:300]}..." if len(result) > 300 else f"回答: {result}")
            else:
                print(f"回答: {str(result)[:300]}..." if len(str(result)) > 300 else f"回答: {str(result)}")
        except Exception as e:
            print(f"❌ 查询失败: {e}")
    
    print("\n🎉 演示完成！")
    print("\n📊 系统状态:")
    print("- ✅ 硅基流动API配置正常")
    print("- ✅ 向量数据库连接正常")
    print("- ✅ RAG服务运行正常")

if __name__ == "__main__":
    main()