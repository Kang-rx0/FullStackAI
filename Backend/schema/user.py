"""Pydantic schemas for user-related endpoints."""

from pydantic import BaseModel, EmailStr, Field


class WelcomeResponse(BaseModel):
    """对 /welcome 接口的响应格式定义"""

    message: str  # 展示给前端的欢迎语
    version: str  # 当前 API 版本号
    docs: str  # Swagger 文档路径
    redoc: str  # ReDoc 文档路径


class RegisterRequest(BaseModel):
    """注册接口的请求体结构"""

    # Field(..., ...) 表示该字段必填，并且可以设置校验规则（长度、描述等）
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)
    email: EmailStr | None = None  # EmailStr 会自动验证邮箱格式
    avatar_url: str | None = None


class LoginRequest(BaseModel):
    """登录接口的请求体结构"""

    username: str
    password: str


class UserResponse(BaseModel):
    """返回给前端的用户基本信息"""

    id: str
    username: str
    email: EmailStr | None = None
    avatar_url: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class AuthResponse(BaseModel):
    """注册/登录成功后统一的响应体"""

    message: str  # 文本提示，例如 "注册成功"
    user: UserResponse  # 内嵌用户信息，避免重复字段定义
