"""
User 数据库模型
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.mysql import CHAR
import uuid

from app.core.database import Base


def generate_uuid():
    """生成 UUID 字符串"""
    return str(uuid.uuid4())


class User(Base):
    """用户表模型"""
    __tablename__ = "users"

    id = Column(CHAR(36), primary_key=True, default=generate_uuid, comment="用户唯一ID")
    username = Column(String(50), unique=True, nullable=False, index=True, comment="用户名")
    email = Column(String(100), unique=True, nullable=True, index=True, comment="邮箱")
    hashed_password = Column(String(255), nullable=False, comment="加密后的密码")
    avatar_url = Column(Text, nullable=True, comment="头像URL")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
