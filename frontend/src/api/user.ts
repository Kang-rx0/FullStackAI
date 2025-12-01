/**
 * 用户相关 API
 */

import request from './request'

export interface LoginRequest {
  account: string
  password: string
}

export interface RegisterRequest {
  username: string
  password: string
  confirmPassword: string
  email?: string
}

export interface UserInfo {
  id: string
  username: string
  email?: string
  avatar_url?: string
  created_at?: string
  updated_at?: string
}

export interface AuthResponse {
  message: string
  token: string
  user: UserInfo
}

// loginAPI 使用 Axios 发起请求
// 响应拦截器已经返回 response.data，所以这里直接返回即可
export function loginAPI(data: LoginRequest): Promise<AuthResponse> {
  return request.post('/aifs/login', data) as unknown as Promise<AuthResponse>
}

export function registerAPI(data: RegisterRequest): Promise<AuthResponse> {
  return request.post('/aifs/register', data) as unknown as Promise<AuthResponse>
}

export function welcomeAPI() {
  return request.get('/aifs/welcome')
}
