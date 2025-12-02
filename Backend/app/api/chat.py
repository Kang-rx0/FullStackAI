"""
聊天相关 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.asynchronous.database import AsyncDatabase
from typing import Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ConversationInfo,
    ConversationDetail,
    ConversationListResponse,
)
from app.schemas.user import MessageResponse
from app.services.chat_service import (
    create_conversation,
    get_conversation_by_id,
    get_user_conversations,
    count_user_conversations,
    add_message_to_conversation,
    update_conversation_title,
    delete_conversation,
    get_conversation_context,
)

# 导入模型
from modelscope import AutoTokenizer, AutoModelForCausalLM

# 模型路径 - 建议后续改为配置文件
MODEL_PATH = r"e:\pythonCode\Model\Qwen\Qwen3-0___6B"

# 延迟加载模型（首次调用时加载）
_model = None
_tokenizer = None


def get_model():
    """获取模型实例（延迟加载）"""
    global _model, _tokenizer
    if _model is None:
        print("🤖 正在加载 AI 模型...")
        _model = AutoModelForCausalLM.from_pretrained(
            MODEL_PATH,
            dtype="auto",
            device_map="auto"
        )
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        print("✅ AI 模型加载完成")
    return _model, _tokenizer


def generate_ai_response(messages: list) -> str:
    """
    调用 AI 模型生成回复
    
    Args:
        messages: 对话历史消息列表
    
    Returns:
        AI 生成的回复文本
    """
    model, tokenizer = get_model()
    
    # 构建对话输入
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=True  # 启用思考模式
    )
    
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    
    # 生成回复
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=32768,
    )
    
    # 提取生成的部分（排除输入）
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
    
    # 解析思考内容，找到 </think> 标记 (151668)
    try:
        index = len(output_ids) - output_ids[::-1].index(151668)
    except ValueError:
        index = 0
    
    # 只返回思考后的实际回复内容
    response = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")
    return response


router = APIRouter()


@router.post("/chat", response_model=ChatResponse, summary="发送聊天消息")
async def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncDatabase = Depends(get_db)
):
    """
    发送聊天消息并获取 AI 回复
    
    - **message**: 用户消息内容
    - **conversation_id**: 会话ID（可选，不传则创建新会话）
    
    返回:
    - **message**: AI 回复内容
    - **conversation_id**: 会话ID
    - **created_at**: 创建时间
    """
    user_id = current_user["id"]
    conversation_id = request.conversation_id
    
    # 如果没有提供会话ID，创建新会话
    if not conversation_id:
        # 使用用户消息的前20个字符作为标题
        title = request.message[:20] + "..." if len(request.message) > 20 else request.message
        conversation = await create_conversation(db, user_id, title)
        conversation_id = conversation["id"]
        context_messages = []
    else:
        # 获取现有会话
        conversation = await get_conversation_by_id(db, conversation_id, user_id)
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="会话不存在或无权访问"
            )
        # 获取历史上下文
        context_messages = get_conversation_context(conversation)
    
    # 保存用户消息
    await add_message_to_conversation(
        db, conversation_id, user_id, "user", request.message
    )
    
    # 构建发送给 AI 的消息列表
    ai_messages = context_messages + [{"role": "user", "content": request.message}]
    
    # 生成 AI 回复
    try:
        ai_response = generate_ai_response(ai_messages)
    except Exception as e:
        print(f"AI 生成错误: {e}")
        ai_response = "抱歉，AI 暂时无法响应，请稍后重试。"
    
    # 保存 AI 回复
    await add_message_to_conversation(
        db, conversation_id, user_id, "assistant", ai_response
    )
    
    return ChatResponse(
        message=ai_response,
        conversation_id=conversation_id
    )


@router.get("/conversations", response_model=ConversationListResponse, summary="获取会话列表")
async def list_conversations(
    skip: int = 0,
    limit: int = 20,
    current_user: dict = Depends(get_current_user),
    db: AsyncDatabase = Depends(get_db)
):
    """
    获取当前用户的会话列表
    
    - **skip**: 跳过数量（分页）
    - **limit**: 获取数量（分页）
    
    返回:
    - **conversations**: 会话列表
    - **total**: 总数量
    """
    user_id = current_user["id"]
    
    conversations = await get_user_conversations(db, user_id, skip, limit)
    total = await count_user_conversations(db, user_id)
    
    # 转换为响应格式
    conv_list = [
        ConversationInfo(
            id=conv["id"],
            title=conv["title"],
            created_at=conv["created_at"],
            updated_at=conv["updated_at"],
            message_count=conv.get("message_count", 0)
        )
        for conv in conversations
    ]
    
    return ConversationListResponse(conversations=conv_list, total=total)


@router.get("/conversations/{conversation_id}", response_model=ConversationDetail, summary="获取会话详情")
async def get_conversation(
    conversation_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncDatabase = Depends(get_db)
):
    """
    获取指定会话的详情（包含所有消息）
    
    - **conversation_id**: 会话ID
    
    返回:
    - 会话详情，包含消息列表
    """
    user_id = current_user["id"]
    
    conversation = await get_conversation_by_id(db, conversation_id, user_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在或无权访问"
        )
    
    return ConversationDetail(
        id=conversation["id"],
        title=conversation["title"],
        created_at=conversation["created_at"],
        updated_at=conversation["updated_at"],
        message_count=len(conversation.get("messages", [])),
        messages=conversation.get("messages", [])
    )


@router.put("/conversations/{conversation_id}/title", response_model=MessageResponse, summary="更新会话标题")
async def update_title(
    conversation_id: str,
    title: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncDatabase = Depends(get_db)
):
    """
    更新会话标题
    
    - **conversation_id**: 会话ID
    - **title**: 新标题
    """
    user_id = current_user["id"]
    
    success = await update_conversation_title(db, conversation_id, user_id, title)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在或无权访问"
        )
    
    return MessageResponse(message="标题更新成功")


@router.delete("/conversations/{conversation_id}", response_model=MessageResponse, summary="删除会话")
async def delete_conv(
    conversation_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncDatabase = Depends(get_db)
):
    """
    删除指定会话
    
    - **conversation_id**: 会话ID
    """
    user_id = current_user["id"]
    
    success = await delete_conversation(db, conversation_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在或无权访问"
        )
    
    return MessageResponse(message="会话删除成功")