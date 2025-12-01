"""
User MongoDB 文档模型
使用 Pydantic 定义数据结构
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

# 这里因为 MongoDB 有一个默认字段 _id 是 ObjectId 类型，
# python和pydantic默认不支持这个类型
# 因此需要定义一个自定义的 Pydantic 类型来处理 ObjectId
class PyObjectId(str):
    """自定义 ObjectId 类型，用于 Pydantic 兼容"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):
        # 如果字段是 ObjectId 类型，转换为字符串
        if isinstance(v, ObjectId):
            return str(v)
        # 如果字段是字符串且是有效的 ObjectId，返回字符串
        if isinstance(v, str) and ObjectId.is_valid(v):
            return v
        raise ValueError("Invalid ObjectId")


class UserInDB(BaseModel):
    """
    数据库中的用户文档模型
    对应 MongoDB users 集合
    """
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    username: str = Field(..., min_length=1, max_length=50)
    email: Optional[str] = Field(default=None, max_length=100)
    hashed_password: str = Field(...)
    avatar_url: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # 这是pydantic的配置类，用于适配MongoDB的ObjectId类型
    class Config:
        populate_by_name = True  # 允许使用 _id 或 id

        # ObjectId不能被JSON序列化
        # 将 ObjectId 转换为字符串以便 JSON 序列化
        json_encoders = {ObjectId: str}


class UserCreate(BaseModel):
    """创建用户时的输入模型"""
    username: str = Field(..., min_length=1, max_length=50)
    email: Optional[str] = None
    password: str = Field(..., min_length=1)


def user_helper(user: dict) -> dict:
    """
    将 MongoDB 文档转换为标准格式
    主要处理 _id 到 id 的映射
    """
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user.get("email"),
        "hashed_password": user["hashed_password"],
        "avatar_url": user.get("avatar_url"),
        "created_at": user.get("created_at"),
        "updated_at": user.get("updated_at"),
    }
