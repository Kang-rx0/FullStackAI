"""
MongoDB 数据库配置和连接管理
使用 PyMongo Async API (替代已弃用的 Motor)
"""
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
from typing import Optional

from app.core.config import settings

# 全局数据库客户端和数据库实例
client: Optional[AsyncMongoClient] = None
db: Optional[AsyncDatabase] = None


async def connect_db():
    """
    连接 MongoDB 数据库
    在应用启动时调用
    """
    global client, db
    print(f"🔗 正在连接 MongoDB: {settings.MONGO_URL}")
    client = AsyncMongoClient(settings.MONGO_URL)
    db = client[settings.MONGO_DB]
    
    # 创建索引（确保唯一性约束）
    await db.users.create_index("username", unique=True)
    await db.users.create_index("email", unique=True, sparse=True)  # sparse 允许 null 值
    
    print(f"✅ MongoDB 连接成功，数据库: {settings.MONGO_DB}")


async def close_db():
    """
    关闭 MongoDB 连接
    在应用关闭时调用
    """
    global client
    if client:
        await client.close()
        print("🔌 MongoDB 连接已关闭")


def get_db() -> AsyncDatabase:
    """
    获取数据库实例
    用于依赖注入
    """
    return db
