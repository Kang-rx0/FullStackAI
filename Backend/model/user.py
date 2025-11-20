"""
用户数据模型
使用 SQLAlchemy ORM 定义用户表结构和操作
"""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
import sys
import os

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import Base
from utils import hash_password, generate_uuid


class User(Base):
    """
    用户数据模型（ORM）
    
    对应数据库表：users
    """
    __tablename__ = 'users'
    
    # 主键（UUID）
    id = Column(String(36), primary_key=True, default=generate_uuid, comment='用户ID (UUID)')
    
    # 用户名（唯一，不能为空）
    username = Column(String(50), unique=True, nullable=False, index=True, comment='用户名')
    
    # 密码哈希（不能为空）
    password_hash = Column(String(255), nullable=False, comment='密码哈希')
    
    # 邮箱（可选，唯一）
    email = Column(String(100), unique=True, nullable=True, index=True, comment='邮箱地址')
    
    # 头像 URL（可选）
    avatar_url = Column(String(500), nullable=True, comment='头像URL')
    
    # 时间戳（自动管理）
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        comment='创建时间'
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment='更新时间'
    )