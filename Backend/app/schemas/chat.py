"""
聊天相关的 Pydantic Schema
用于请求/响应数据验证
"""
from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, Field


# ==================== 消息相关 ====================

class MessageBase(BaseModel):
    """消息基础结构"""
    role: Literal["user", "assistant", "system"] = Field(..., description="消息角色")
    content: str = Field(..., description="消息内容")


class ChatMessage(MessageBase):
    """完整的聊天消息（包含时间戳）"""
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ==================== 请求 Schema ====================

class ChatRequest(BaseModel):
    """聊天请求"""
    message: str = Field(..., min_length=1, description="用户消息内容")
    conversation_id: Optional[str] = Field(default=None, description="会话ID，不传则创建新会话")


# ==================== 响应 Schema ====================

class ChatResponse(BaseModel):
    """聊天响应"""
    message: str = Field(..., description="AI回复内容")
    conversation_id: str = Field(..., description="会话ID")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationInfo(BaseModel):
    """会话信息"""
    id: str = Field(..., description="会话ID")
    title: str = Field(..., description="会话标题")
    created_at: datetime
    updated_at: datetime
    message_count: int = Field(default=0, description="消息数量")


class ConversationDetail(ConversationInfo):
    """会话详情（包含消息列表）"""
    messages: List[ChatMessage] = Field(default=[], description="消息列表")


class ConversationListResponse(BaseModel):
    """会话列表响应"""
    conversations: List[ConversationInfo]
    total: int
