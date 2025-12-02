/**
 * 聊天相关 API
 */

import request from './request'

// ==================== 类型定义 ====================

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system'
  content: string
  created_at?: string
}

export interface ChatRequest {
  message: string
  conversation_id?: string | null
}

export interface ChatResponse {
  message: string
  conversation_id: string
  created_at: string
}

export interface ConversationInfo {
  id: string
  title: string
  created_at: string
  updated_at: string
  message_count: number
}

export interface ConversationDetail extends ConversationInfo {
  messages: ChatMessage[]
}

export interface ConversationListResponse {
  conversations: ConversationInfo[]
  total: number
}

export interface MessageResponse {
  message: string
}

// ==================== API 函数 ====================

/**
 * 发送聊天消息
 */
export function sendMessageAPI(data: ChatRequest): Promise<ChatResponse> {
  return request.post('/aifs/chat', data) as unknown as Promise<ChatResponse>
}

/**
 * 获取会话列表
 */
export function getConversationsAPI(skip = 0, limit = 20): Promise<ConversationListResponse> {
  return request.get('/aifs/conversations', { params: { skip, limit } }) as unknown as Promise<ConversationListResponse>
}

/**
 * 获取会话详情（包含消息列表）
 */
export function getConversationDetailAPI(conversationId: string): Promise<ConversationDetail> {
  return request.get(`/aifs/conversations/${conversationId}`) as unknown as Promise<ConversationDetail>
}

/**
 * 更新会话标题
 */
export function updateConversationTitleAPI(conversationId: string, title: string): Promise<MessageResponse> {
  return request.put(`/aifs/conversations/${conversationId}/title`, null, {
    params: { title }
  }) as unknown as Promise<MessageResponse>
}

/**
 * 删除会话
 */
export function deleteConversationAPI(conversationId: string): Promise<MessageResponse> {
  return request.delete(`/aifs/conversations/${conversationId}`) as unknown as Promise<MessageResponse>
}
