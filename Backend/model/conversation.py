"""
会话数据模型
使用 SQLAlchemy ORM 定义会话表结构和操作
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Text, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from typing import Optional
import sys
import os

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import Base
from utils import generate_uuid


class Conversation(Base):
    """
    会话数据模型（ORM）
    
    对应数据库表：conversations
    """
    __tablename__ = 'conversations'
    
    # 主键（UUID）
    id = Column(String(36), primary_key=True, default=generate_uuid, comment='会话ID (UUID)')
    
    # 外键：关联用户（UUID）
    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True, comment='用户ID')
    
    # 会话标题
    title = Column(String(255), nullable=True, comment='会话标题')
    
    # AI 模型配置
    model_name = Column(String(50), nullable=False, default='gpt-3.5-turbo', comment='使用的AI模型')
    system_prompt = Column(Text, nullable=True, comment='系统提示词')
    temperature = Column(Float, nullable=False, default=0.7, comment='温度参数')
    max_tokens = Column(Integer, nullable=False, default=2000, comment='最大token数')
    
    # 统计信息
    message_count = Column(Integer, nullable=False, default=0, comment='消息数量')
    
    # 时间戳
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment='更新时间')
    
    # 关系映射（可选，用于关联查询）
    # user = relationship("User", back_populates="conversations")
    # messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        """字符串表示"""
        return f"<Conversation(id={self.id}, title='{self.title}', user_id={self.user_id})>"
    
    def to_dict(self) -> dict:
        """
        转换为字典（用于 API 响应）
        
        Returns:
            dict: 会话信息字典
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'model_name': self.model_name,
            'system_prompt': self.system_prompt,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'message_count': self.message_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


# 会话数据访问层
class ConversationRepository:
    """
    会话数据仓库
    封装常用的数据库操作
    """
    
    @staticmethod
    def get_by_id(db, conversation_id: str) -> Optional[Conversation]:
        """根据 ID 查询会话"""
        return db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    @staticmethod
    def get_by_user(db, user_id: str, skip: int = 0, limit: int = 50):
        """
        获取用户的所有会话（支持分页）
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            list: 会话列表
        """
        return db.query(Conversation)\
            .filter(Conversation.user_id == user_id)\
            .order_by(Conversation.updated_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    @staticmethod
    def count_by_user(db, user_id: str) -> int:
        """统计用户的会话总数"""
        return db.query(Conversation).filter(Conversation.user_id == user_id).count()
    
    @staticmethod
    def create(db, user_id: str, title: Optional[str] = None, 
               model_name: str = 'gpt-3.5-turbo',
               system_prompt: Optional[str] = None,
               temperature: float = 0.7,
               max_tokens: int = 2000) -> Conversation:
        """
        创建新会话
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            title: 会话标题
            model_name: AI模型名称
            system_prompt: 系统提示词
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            Conversation: 创建的会话对象
        """
        conversation = Conversation(
            user_id=user_id,
            title=title or f"新会话",
            model_name=model_name,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation
    
    @staticmethod
    def update(db, conversation: Conversation) -> Conversation:
        """
        更新会话信息
        
        Args:
            db: 数据库会话
            conversation: 会话对象
            
        Returns:
            Conversation: 更新后的会话对象
        """
        db.commit()
        db.refresh(conversation)
        return conversation
    
    @staticmethod
    def delete(db, conversation_id: str) -> bool:
        """
        删除会话
        
        Args:
            db: 数据库会话
            conversation_id: 会话ID
            
        Returns:
            bool: 是否删除成功
        """
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation:
            db.delete(conversation)
            db.commit()
            return True
        return False
    
    @staticmethod
    def increment_message_count(db, conversation_id: str):
        """增加消息计数"""
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation:
            conversation.message_count += 1
            db.commit()
