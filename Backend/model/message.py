"""
消息数据模型
使用 SQLAlchemy ORM 定义消息表结构和操作
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from typing import Optional, List
import sys
import os

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import Base
from utils import generate_uuid


class Message(Base):
    """
    消息数据模型（ORM）
    
    对应数据库表：messages
    """
    __tablename__ = 'messages'
    
    # 主键（UUID）
    id = Column(String(36), primary_key=True, default=generate_uuid, comment='消息ID (UUID)')
    
    # 外键：关联会话（UUID）
    conversation_id = Column(
        String(36), 
        ForeignKey('conversations.id', ondelete='CASCADE'), 
        nullable=False, 
        index=True, 
        comment='会话ID'
    )
    
    # 消息角色（user/assistant/system）
    role = Column(String(50), nullable=False, comment='消息角色')
    
    # 消息内容
    content = Column(Text, nullable=False, comment='消息内容')
    
    # AI 模型信息（仅 assistant 角色）
    model = Column(String(50), nullable=True, comment='使用的AI模型')
    tokens_used = Column(Integer, nullable=True, comment='使用的token数')
    
    # 时间戳
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment='创建时间')
    
    # 关系映射（可选）
    # conversation = relationship("Conversation", back_populates="messages")