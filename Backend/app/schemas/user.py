"""
用户相关的 Pydantic Schema
用于请求/响应数据验证
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


# ==================== 请求 Schema ====================

class LoginRequest(BaseModel):
    """登录请求"""
    account: str  # 可以是用户名或邮箱
    password: str


class RegisterRequest(BaseModel):
    """注册请求"""
    username: str
    password: str
    email: Optional[EmailStr] = None


# ==================== 响应 Schema ====================

class UserInfo(BaseModel):
    """用户信息（不包含密码）"""
    id: str
    username: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # 支持从 ORM 模型转换


class AuthResponse(BaseModel):
    """认证响应（登录/注册成功后返回）"""
    message: str
    token: str
    user: UserInfo


class MessageResponse(BaseModel):
    """通用消息响应"""
    message: str
