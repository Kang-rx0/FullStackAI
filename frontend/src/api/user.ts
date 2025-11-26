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

export function loginAPI(data: LoginRequest) {
  return request.post<AuthResponse>('/aifs/login', data)
}

export function registerAPI(data: RegisterRequest) {
  return request.post<AuthResponse>('/aifs/register', data)
}

export function welcomeAPI() {
  return request.get('/aifs/welcome')
}
