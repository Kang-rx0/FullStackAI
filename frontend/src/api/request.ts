import axios from 'axios'

// 后端 API 基础地址
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// 创建 axios 实例
const instance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000,  // 5分钟超时，AI 生成需要较长时间
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器：自动加 token
instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截器：统一处理错误
instance.interceptors.response.use(
  (response) => response.data,
  (error) => {
    // 可统一弹窗/跳转等
    return Promise.reject(error.response?.data || error)
  }
)

export default instance
