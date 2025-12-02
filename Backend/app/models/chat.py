"""
聊天相关的 MongoDB 文档模型
"""
from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, Field
from bson import ObjectId

from app.models.user import PyObjectId


class MessageInDB(BaseModel):
    """数据库中的消息结构"""
    role: Literal["user", "assistant", "system"]
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationInDB(BaseModel):
    """
    数据库中的会话文档模型
    对应 MongoDB conversations 集合
    """
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: str = Field(..., description="用户ID")
    title: str = Field(default="新对话", max_length=100, description="会话标题")
    messages: List[MessageInDB] = Field(default=[], description="消息列表")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


def conversation_helper(conversation: dict) -> dict:
    """
    将 MongoDB 文档转换为标准字典格式
    
    Args:
        conversation: MongoDB 文档
    
    Returns:
        转换后的字典，包含 id 字段
    """
    return {
        "id": str(conversation["_id"]),
        "user_id": conversation["user_id"],
        "title": conversation.get("title", "新对话"),
        "messages": conversation.get("messages", []),
        "created_at": conversation.get("created_at"),
        "updated_at": conversation.get("updated_at"),
    }
