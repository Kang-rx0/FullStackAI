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

// loginAPI 使用 Axios 发起请求，默认返回的是 AxiosResponse
// promise<AuthResponse>是为了将返回类型从 AxiosResponse 转换为 AuthResponse
// 此外，最后通过 .then 提取了AxiosResponse类型的data属性 res.data，
// 这里面的才是被转换成了 AuthResponse 类型的数据
export function loginAPI(data: LoginRequest):Promise<AuthResponse> {
  return request.post<AuthResponse>('/aifs/login', data).then((res) => res.data)
}

export function registerAPI(data: RegisterRequest):Promise<AuthResponse> {
  return request.post<AuthResponse>('/aifs/register', data).then((res) => res.data)
}

export function welcomeAPI() {
  return request.get('/aifs/welcome')
}
