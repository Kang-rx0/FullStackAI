"""
用户认证相关 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.asynchronous.database import AsyncDatabase

from app.core.database import get_db
from app.core.security import create_access_token
from app.schemas.user import (
    LoginRequest,
    RegisterRequest,
    AuthResponse,
    UserInfo,
    MessageResponse
)
from app.services.user_service import (
    authenticate_user,
    create_user,
    get_user_by_username,
    get_user_by_email
)

router = APIRouter()


@router.post("/login", response_model=AuthResponse, summary="用户登录")
async def login(request: LoginRequest, db: AsyncDatabase = Depends(get_db)):
    """
    用户登录接口
    
    - **account**: 账号（用户名或邮箱）
    - **password**: 密码
    
    返回:
    - **message**: 成功消息
    - **token**: JWT token
    - **user**: 用户信息
    """
    # 验证用户身份
    user = await authenticate_user(db, request.account, request.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="账号或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 生成 JWT token
    access_token = create_access_token(data={"sub": user["id"], "username": user["username"]})
    
    # 构建用户信息响应
    user_info = UserInfo(
        id=user["id"],
        username=user["username"],
        email=user.get("email"),
        avatar_url=user.get("avatar_url"),
        created_at=user.get("created_at"),
        updated_at=user.get("updated_at")
    )
    
    return AuthResponse(
        message="登录成功",
        token=access_token,
        user=user_info
    )


@router.get("/welcome", response_model=MessageResponse, summary="欢迎接口")
async def welcome():
    """
    欢迎接口，用于测试 API 是否正常工作
    """
    return MessageResponse(message="欢迎使用 AI FullStack API！")


@router.post("/register", response_model=AuthResponse, summary="用户注册")
async def register(request: RegisterRequest, db: AsyncDatabase = Depends(get_db)):
    """
    用户注册接口
    
    - **username**: 用户名
    - **password**: 密码
    - **email**: 邮箱（可选）
    
    返回:
    - **message**: 成功消息
    - **token**: JWT token
    - **user**: 用户信息
    """
    # 检查用户名是否已存在
    if await get_user_by_username(db, request.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否已存在
    if request.email and await get_user_by_email(db, request.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 创建新用户
    user = await create_user(
        db,
        username=request.username,
        password=request.password,
        email=request.email
    )
    
    # 生成 JWT token
    access_token = create_access_token(data={"sub": user["id"], "username": user["username"]})
    
    # 构建用户信息响应
    user_info = UserInfo(
        id=user["id"],
        username=user["username"],
        email=user.get("email"),
        avatar_url=user.get("avatar_url"),
        created_at=user.get("created_at"),
        updated_at=user.get("updated_at")
    )
    
    return AuthResponse(
        message="注册成功",
        token=access_token,
        user=user_info
    )
