/**
 * API 基础配置
 * 定义后端服务地址和通用请求设置
 */

// 后端 API 基础地址（开发环境）
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// 通用请求头
export const DEFAULT_HEADERS = {
  'Content-Type': 'application/json',
}

/**
 * 封装 fetch 请求
 * @param endpoint API 端点（相对路径，如 '/aifs/login'）
 * @param options fetch 选项
 */
export async function request<T = any>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`
  
  const config: RequestInit = {
    ...options,
    headers: {
      ...DEFAULT_HEADERS,
      ...options.headers,
    },
  }

  try {
    const response = await fetch(url, config)
    
    // 处理 HTTP 错误状态
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: response.statusText }))
      throw new Error(errorData.detail || `HTTP ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error('API 请求失败:', error)
    throw error
  }
}
