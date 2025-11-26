/**
 * 用户相关 API
 * 对接后端 FastAPI 的用户接口（/aifs/...）
 */

import { request } from './request'

// ========== 类型定义 ==========

/** 登录请求参数 */
export interface LoginRequest {
  username: string
  password: string
}

/** 注册请求参数 */
export interface RegisterRequest {
  username: string
  password: string
  email?: string
  avatar_url?: string
}

/** 用户信息 */
export interface UserInfo {
  id: string
  username: string
  email?: string
  avatar_url?: string
  created_at?: string
  updated_at?: string
}

/** 认证响应（登录/注册） */
export interface AuthResponse {
  message: string
  user: UserInfo
}

// ========== API 函数 ==========

/**
 * 用户登录
 * POST /aifs/login
 */
export async function loginAPI(data: LoginRequest): Promise<AuthResponse> {
  return request<AuthResponse>('/aifs/login', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

/**
 * 用户注册
 * POST /aifs/register
 */
export async function registerAPI(data: RegisterRequest): Promise<AuthResponse> {
  return request<AuthResponse>('/aifs/register', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

/**
 * 获取欢迎信息（可选，用于测试连接）
 * GET /aifs/welcome
 */
export async function getWelcomeAPI() {
  return request('/aifs/welcome', { method: 'GET' })
}
