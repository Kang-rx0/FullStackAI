<script setup lang="ts">
import { ref, onMounted, nextTick, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  sendMessageAPI, 
  getConversationsAPI, 
  getConversationDetailAPI,
  deleteConversationAPI,
  type ChatMessage,
  type ConversationInfo 
} from '@/api/chat'

const router = useRouter()

// ==================== 状态管理 ====================

// 当前用户信息
const userInfo = computed(() => {
  const user = localStorage.getItem('user')
  return user ? JSON.parse(user) : null
})

// 会话列表
const conversations = ref<ConversationInfo[]>([])
const conversationsLoading = ref(false)

// 当前会话
const currentConversationId = ref<string | null>(null)
const messages = ref<ChatMessage[]>([])

// 输入框
const inputMessage = ref('')
const sending = ref(false)

// 消息列表容器引用
const messagesContainer = ref<HTMLElement | null>(null)

// ==================== 生命周期 ====================

onMounted(async () => {
  // 检查登录状态
  const token = localStorage.getItem('token')
  if (!token) {
    ElMessage.warning('请先登录')
    router.push('/aifs/login')
    return
  }
  
  // 加载会话列表
  await loadConversations()
})

// ==================== 会话管理 ====================

/**
 * 加载会话列表
 */
async function loadConversations() {
  conversationsLoading.value = true
  try {
    const res = await getConversationsAPI()
    conversations.value = res.conversations
  } catch (error: any) {
    console.error('加载会话列表失败:', error)
    if (error.detail === '无效的认证凭证') {
      ElMessage.error('登录已过期，请重新登录')
      router.push('/aifs/login')
    }
  } finally {
    conversationsLoading.value = false
  }
}

/**
 * 创建新会话
 */
function createNewConversation() {
  currentConversationId.value = null
  messages.value = []
  inputMessage.value = ''
}

/**
 * 选择会话
 */
async function selectConversation(conv: ConversationInfo) {
  if (currentConversationId.value === conv.id) return
  
  currentConversationId.value = conv.id
  
  try {
    const detail = await getConversationDetailAPI(conv.id)
    messages.value = detail.messages
    await scrollToBottom()
  } catch (error) {
    console.error('加载会话详情失败:', error)
    ElMessage.error('加载会话失败')
  }
}

/**
 * 删除会话
 */
async function handleDeleteConversation(conv: ConversationInfo) {
  try {
    await ElMessageBox.confirm(
      `确定要删除会话"${conv.title}"吗？`,
      '删除确认',
      { type: 'warning' }
    )
    
    await deleteConversationAPI(conv.id)
    ElMessage.success('删除成功')
    
    // 如果删除的是当前会话，清空消息
    if (currentConversationId.value === conv.id) {
      createNewConversation()
    }
    
    // 重新加载列表
    await loadConversations()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除会话失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// ==================== 消息发送 ====================

/**
 * 发送消息
 */
async function sendMessage() {
  const content = inputMessage.value.trim()
  if (!content || sending.value) return
  
  // 添加用户消息到界面
  messages.value.push({
    role: 'user',
    content: content,
    created_at: new Date().toISOString()
  })
  
  inputMessage.value = ''
  sending.value = true
  await scrollToBottom()
  
  // 添加一个"正在输入"的占位消息
  const thinkingIndex = messages.value.length
  messages.value.push({
    role: 'assistant',
    content: '正在思考...',
    created_at: new Date().toISOString()
  })
  
  try {
    const res = await sendMessageAPI({
      message: content,
      conversation_id: currentConversationId.value
    })
    
    // 更新当前会话ID（如果是新会话）
    if (!currentConversationId.value) {
      currentConversationId.value = res.conversation_id
      // 刷新会话列表
      await loadConversations()
    }
    
    // 更新 AI 回复
    messages.value[thinkingIndex] = {
      role: 'assistant',
      content: res.message,
      created_at: res.created_at
    }
    
  } catch (error: any) {
    console.error('发送消息失败:', error)
    // 移除"正在输入"消息
    messages.value.splice(thinkingIndex, 1)
    ElMessage.error(error.detail || '发送失败，请重试')
  } finally {
    sending.value = false
    await scrollToBottom()
  }
}

/**
 * 按回车发送
 */
function handleKeydown(event: KeyboardEvent) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}

/**
 * 滚动到底部
 */
async function scrollToBottom() {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// ==================== 退出登录 ====================

function handleLogout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/aifs/login')
}

/**
 * 格式化时间
 */
function formatTime(dateStr: string) {
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<template>
  <div class="chat-container">
    <!-- 左侧边栏：会话列表 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2>对话列表</h2>
        <el-button type="primary" size="small" @click="createNewConversation">
          新建对话
        </el-button>
      </div>
      
      <div class="conversation-list" v-loading="conversationsLoading">
        <div
          v-for="conv in conversations"
          :key="conv.id"
          class="conversation-item"
          :class="{ active: currentConversationId === conv.id }"
          @click="selectConversation(conv)"
        >
          <div class="conv-info">
            <div class="conv-title">{{ conv.title }}</div>
            <div class="conv-meta">{{ conv.message_count }} 条消息</div>
          </div>
          <el-button
            type="danger"
            size="small"
            text
            @click.stop="handleDeleteConversation(conv)"
          >
            删除
          </el-button>
        </div>
        
        <div v-if="!conversationsLoading && conversations.length === 0" class="empty-tip">
          暂无对话，点击上方按钮开始
        </div>
      </div>
      
      <!-- 用户信息 -->
      <div class="sidebar-footer">
        <div class="user-info">
          <el-avatar :size="32">{{ userInfo?.username?.[0] || 'U' }}</el-avatar>
          <span class="username">{{ userInfo?.username || '用户' }}</span>
        </div>
        <el-button type="text" @click="handleLogout">退出</el-button>
      </div>
    </aside>
    
    <!-- 右侧：聊天区域 -->
    <main class="chat-main">
      <!-- 消息列表 -->
      <div class="messages-container" ref="messagesContainer">
        <div v-if="messages.length === 0" class="welcome-message">
          <h3>👋 你好！我是 AI 助手</h3>
          <p>有什么可以帮助你的吗？</p>
        </div>
        
        <div
          v-for="(msg, index) in messages"
          :key="index"
          class="message-item"
          :class="msg.role"
        >
          <div class="message-avatar">
            <el-avatar v-if="msg.role === 'user'" :size="36">
              {{ userInfo?.username?.[0] || 'U' }}
            </el-avatar>
            <el-avatar v-else :size="36" style="background: #409eff;">AI</el-avatar>
          </div>
          <div class="message-content">
            <div class="message-text">{{ msg.content }}</div>
            <div class="message-time" v-if="msg.created_at">
              {{ formatTime(msg.created_at) }}
            </div>
          </div>
        </div>
      </div>
      
      <!-- 输入框 -->
      <div class="input-area">
        <el-input
          v-model="inputMessage"
          type="textarea"
          :rows="2"
          placeholder="输入消息，按 Enter 发送..."
          :disabled="sending"
          @keydown="handleKeydown"
        />
        <el-button
          type="primary"
          :loading="sending"
          :disabled="!inputMessage.trim()"
          @click="sendMessage"
        >
          发送
        </el-button>
      </div>
    </main>
  </div>
</template>

<style scoped>
.chat-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  background: #f5f7fa;
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
}

/* 左侧边栏 */
.sidebar {
  width: 260px;
  min-width: 260px;
  max-width: 260px;
  background: #fff;
  border-right: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.conversation-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.conversation-item {
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
  transition: background 0.2s;
}

.conversation-item:hover {
  background: #f5f7fa;
}

.conversation-item.active {
  background: #ecf5ff;
}

.conv-info {
  flex: 1;
  overflow: hidden;
}

.conv-title {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.conv-meta {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.empty-tip {
  text-align: center;
  color: #909399;
  padding: 20px;
  font-size: 14px;
}

.sidebar-footer {
  padding: 12px 16px;
  border-top: 1px solid #e4e7ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.username {
  font-size: 14px;
  font-weight: 500;
}

/* 右侧聊天区域 */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-width: 0;  /* 防止 flex 子元素撑开 */
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px 40px;
  min-height: 0;  /* 关键：允许 flex 子元素收缩 */
}

.welcome-message {
  text-align: center;
  color: #606266;
  margin-top: 100px;
}

.welcome-message h3 {
  font-size: 24px;
  margin-bottom: 8px;
}

.message-item {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  max-width: 70%;
}

.message-item.user {
  flex-direction: row-reverse;
  margin-left: auto;
  margin-right: 0;
}

.message-item.assistant {
  margin-right: auto;
  margin-left: 0;
}

.message-content {
  flex: 1;
}

.message-item.user .message-content {
  text-align: right;
}

.message-text {
  display: inline-block;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

.message-item.user .message-text {
  background: #409eff;
  color: #fff;
  border-bottom-right-radius: 4px;
}

.message-item.assistant .message-text {
  background: #fff;
  border: 1px solid #e4e7ed;
  border-bottom-left-radius: 4px;
}

.message-time {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

/* 输入区域 */
.input-area {
  padding: 16px 40px;
  background: #fff;
  border-top: 1px solid #e4e7ed;
  display: flex;
  gap: 12px;
  align-items: flex-end;
  flex-shrink: 0;  /* 防止输入区域被压缩 */
}

.input-area .el-textarea {
  flex: 1;
}

.input-area .el-button {
  height: 54px;
  padding: 0 24px;
}
</style>