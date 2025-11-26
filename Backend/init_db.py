"""
数据库初始化脚本
用于创建数据库表
"""
import sys
import os

# 添加 backend 目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import init_db


def init_database():
    """初始化数据库表"""
    print("🔧 正在初始化数据库表...")
    init_db()
    print("✅ 数据库表创建完成")


if __name__ == "__main__":
    print("=" * 50)
    print("AI FullStack 数据库初始化脚本")
    print("=" * 50)
    
    init_database()
    
    print("=" * 50)
    print("🎉 初始化完成！")
    print("=" * 50)
