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

@router.post("/register", response_model=AuthResponse, summary="用户注册")
async def register(request: RegisterRequest, db: AsyncDatabase = Depends(get_db)):
    """
    用户注册接口
    
    - **username**: 用户名
    - **email**: 邮箱
    - **password**: 密码
    
    返回:
    - **message**: 成功消息
    - **token**: JWT token
    - **user**: 用户信息
    """
    # 检查用户名是否已存在
    existing_user = await get_user_by_username(db, request.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已被占用"
        )
    
    # 如果提供了邮箱，检查邮箱是否已存在
    if request.email:
        existing_email_user = await get_user_by_email(db, request.email)
        if existing_email_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被注册"
            )
    
    # 创建新用户
    user = await create_user(db, request.username, request.password, request.email)
    
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