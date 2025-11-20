"""用户相关 API"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db import get_db
from schema.user import (
    WelcomeResponse,
    RegisterRequest,
    LoginRequest,
    UserResponse,
    AuthResponse,
)
from .utils import (
    ensure_unique_user,
    create_user_model,
    authenticate_user,
    serialize_user,
)


# APIRouter 用来把一组相关接口集中管理；prefix 会自动给所有路由加上 "/aifs" 前缀
# tags 让接口在 Swagger 文档里分组，responses 可预先声明通用响应
router = APIRouter(
    prefix="/aifs",
    tags=["用户"],
    responses={404: {"description": "Not found"}},
)


@router.get("/welcome", response_model=WelcomeResponse)
async def welcome():
    """欢迎信息端点"""
    return WelcomeResponse(
        message="欢迎使用 AI 对话系统 API",
        version="1.0.0",
        docs="/docs",
        redoc="/redoc",
    )


@router.post(
    "/register",
    response_model=AuthResponse,  # response_model 会在返回时套用 AuthResponse schema，确保响应字段和类型正确
    status_code=status.HTTP_201_CREATED,  # 显式声明 201，表示资源创建成功
)
async def register_user(
    payload: RegisterRequest,  # payload 指向请求体，FastAPI 会自动将 JSON 解析成 RegisterRequest 实例
    db: Session = Depends(get_db),  # Depends 注入一个数据库会话，生命周期由 get_db 控制
):
    """注册新用户"""
    ensure_unique_user(db, payload.username, payload.email)

    user = create_user_model(
        username=payload.username,
        password=payload.password,
        email=payload.email,
        avatar_url=payload.avatar_url,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return AuthResponse(
        message="注册成功",
        user=UserResponse(**serialize_user(user))
    )


@router.post(
    "/login",
    response_model=AuthResponse,  # FastAPI 将登录成功结果包装成 AuthResponse，减少手动构造 JSON 的工作
)
async def login_user(
    payload: LoginRequest,  # 自动解析 JSON 中的用户名和密码
    db: Session = Depends(get_db),  # 依赖注入数据库会话
):
    """用户登录"""
    user = authenticate_user(db, payload.username, payload.password)
    return AuthResponse(
        message="登录成功",
        user=UserResponse(**serialize_user(user))
    )