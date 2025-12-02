"""
聊天相关业务逻辑服务
使用 PyMongo Async API
"""
from datetime import datetime
from typing import Optional, List
from pymongo.asynchronous.database import AsyncDatabase
from bson import ObjectId

from app.models.chat import conversation_helper


async def create_conversation(
    db: AsyncDatabase,
    user_id: str,
    title: str = "新对话"
) -> dict:
    """
    创建新会话
    
    Args:
        db: MongoDB 数据库实例
        user_id: 用户ID
        title: 会话标题
    
    Returns:
        新创建的会话字典
    """
    now = datetime.utcnow()
    conversation_doc = {
        "user_id": user_id,
        "title": title,
        "messages": [],
        "created_at": now,
        "updated_at": now,
    }
    
    result = await db.conversations.insert_one(conversation_doc)
    conversation_doc["_id"] = result.inserted_id
    
    return conversation_helper(conversation_doc)


async def get_conversation_by_id(
    db: AsyncDatabase,
    conversation_id: str,
    user_id: str
) -> Optional[dict]:
    """
    根据ID获取会话（需验证用户归属）
    
    Args:
        db: MongoDB 数据库实例
        conversation_id: 会话ID
        user_id: 用户ID（验证归属）
    
    Returns:
        会话字典，不存在或不属于该用户则返回 None
    """
    try:
        conversation = await db.conversations.find_one({
            "_id": ObjectId(conversation_id),
            "user_id": user_id
        })
        if conversation:
            return conversation_helper(conversation)
    except:
        pass
    return None


async def get_user_conversations(
    db: AsyncDatabase,
    user_id: str,
    skip: int = 0,
    limit: int = 20
) -> List[dict]:
    """
    获取用户的所有会话列表
    
    Args:
        db: MongoDB 数据库实例
        user_id: 用户ID
        skip: 跳过数量（分页）
        limit: 获取数量（分页）
    
    Returns:
        会话列表
    """
    cursor = db.conversations.find(
        {"user_id": user_id}
    ).sort("updated_at", -1).skip(skip).limit(limit)
    
    conversations = []
    async for conv in cursor:
        conv_dict = conversation_helper(conv)
        # 添加消息数量
        conv_dict["message_count"] = len(conv.get("messages", []))
        conversations.append(conv_dict)
    
    return conversations


async def count_user_conversations(db: AsyncDatabase, user_id: str) -> int:
    """统计用户的会话数量"""
    return await db.conversations.count_documents({"user_id": user_id})


async def add_message_to_conversation(
    db: AsyncDatabase,
    conversation_id: str,
    user_id: str,
    role: str,
    content: str
) -> bool:
    """
    向会话添加消息
    
    Args:
        db: MongoDB 数据库实例
        conversation_id: 会话ID
        user_id: 用户ID（验证归属）
        role: 消息角色 (user/assistant/system)
        content: 消息内容
    
    Returns:
        是否添加成功
    """
    try:
        message = {
            "role": role,
            "content": content,
            "created_at": datetime.utcnow()
        }
        
        result = await db.conversations.update_one(
            {
                "_id": ObjectId(conversation_id),
                "user_id": user_id
            },
            {
                "$push": {"messages": message},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        return result.modified_count > 0
    except:
        return False


async def update_conversation_title(
    db: AsyncDatabase,
    conversation_id: str,
    user_id: str,
    title: str
) -> bool:
    """
    更新会话标题
    
    Args:
        db: MongoDB 数据库实例
        conversation_id: 会话ID
        user_id: 用户ID（验证归属）
        title: 新标题
    
    Returns:
        是否更新成功
    """
    try:
        result = await db.conversations.update_one(
            {
                "_id": ObjectId(conversation_id),
                "user_id": user_id
            },
            {
                "$set": {
                    "title": title,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    except:
        return False


async def delete_conversation(
    db: AsyncDatabase,
    conversation_id: str,
    user_id: str
) -> bool:
    """
    删除会话
    
    Args:
        db: MongoDB 数据库实例
        conversation_id: 会话ID
        user_id: 用户ID（验证归属）
    
    Returns:
        是否删除成功
    """
    try:
        result = await db.conversations.delete_one({
            "_id": ObjectId(conversation_id),
            "user_id": user_id
        })
        return result.deleted_count > 0
    except:
        return False


def get_conversation_context(conversation: dict, max_messages: int = 10) -> List[dict]:
    """
    获取会话的上下文消息（用于发送给AI）
    
    Args:
        conversation: 会话字典
        max_messages: 最大消息数量
    
    Returns:
        消息列表（只包含 role 和 content）
    """
    messages = conversation.get("messages", [])
    # 获取最近的消息作为上下文
    recent_messages = messages[-max_messages:] if len(messages) > max_messages else messages
    
    return [{"role": msg["role"], "content": msg["content"]} for msg in recent_messages]
