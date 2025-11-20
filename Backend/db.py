"""
数据库配置模块
使用 SQLAlchemy ORM 进行数据库操作
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# 数据库连接配置
DATABASE_URL = "mysql+pymysql://root:0406@localhost:3306/aifs"

# 创建数据库引擎
# echo=True 会打印 SQL 语句（开发时有用，生产环境设为 False）
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,  # 连接前检测连接是否有效
    pool_recycle=3600,   # 1小时后回收连接
)

# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 创建基类（所有模型类都继承这个基类）
Base = declarative_base()


# 依赖注入函数：获取数据库会话
def get_db() -> Generator[Session, None, None]:
    """
    FastAPI 依赖注入函数
    为每个请求创建独立的数据库会话
    请求结束后自动关闭会话
    
    Yields:
        Session: SQLAlchemy 数据库会话
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


