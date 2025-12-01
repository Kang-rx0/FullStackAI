<script setup lang="ts">
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { loginAPI } from '@/api/user'
import { useRouter } from 'vue-router'

interface LoginForm {
  account: string
  password: string
}

const router = useRouter()

// 把表单对象的节点设置为FormInstance类型
const formRef = ref<FormInstance>()
const form = reactive<LoginForm>({ account: '', password: '' })
const loading = ref(false)

const rules: FormRules<LoginForm> = {
  account: [{ required: true, message: '请输入账号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

const onSubmit = async () => {
  // 确保 formRef 已经被赋值
  if (!formRef.value) return
  
  // formRef.value.validate 是 Element Plus 提供的表单校验方法
  // 它接受一个回调函数 (valid) => { ... }
  // valid 参数由 Element Plus 自动传入：
  //   - true：所有字段通过校验
  //   - false：至少一个字段未通过校验
  await formRef.value.validate(async (valid) => {
    if (!valid) return // 校验失败，提前返回
    
    loading.value = true
    try {
      // 调用后端登录接口 POST /aifs/login
      const response = await loginAPI({
        account: form.account,
        password: form.password,
      })
      
      // 登录成功
      ElMessage.success(response.message || '登录成功')
      
      // 存储用户信息到 localStorage（后续可改为 pinia store）
      localStorage.setItem('user', JSON.stringify(response.user))
      localStorage.setItem('token', response.token)
      
      // TODO: 跳转到主页或聊天页面
      console.log('登录成功，用户信息：', response.user)
      
    } catch (error: any) {
      // 登录失败，显示错误信息
      ElMessage.error(error.message || '登录失败，请检查用户名和密码')
      console.error('登录失败：', error)
    } finally {
      loading.value = false
    }
  })
}

const onRegister = () => {
  router.push('/aifs/register')
}

const onForgot = () => {
  // 占位：跳转到忘记密码页（后续接入）
}
</script>

<template>
  <div class="login-page">
    <el-card class="login-card" shadow="hover">
      <template #header>
        <div class="card-header">登录</div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        class="form"
      >
        <el-form-item label="账号" prop="account">
          <el-input
            v-model.trim="form.account"
            placeholder="请输入账号"
            autocomplete="username"
          />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model.trim="form.password"
            type="password"
            show-password
            placeholder="请输入密码"
            autocomplete="current-password"
          />
        </el-form-item>

        <el-button
          type="primary"
          class="submit-btn"
          :loading="loading"
          @click="onSubmit"
        >登录</el-button>

        <div class="links">
          <el-link type="primary" :underline="false" @click="onRegister">注册</el-link>
          <el-link type="primary" :underline="false" @click="onForgot">忘记密码</el-link>
        </div>
      </el-form>
    </el-card>
  </div>
  
</template>

<style scoped>
/* 整页居中背景 */
.login-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: radial-gradient(ellipse at top, #f6faff 0%, #eef3fb 60%, #e8eef9 100%);
  padding: 16px;
}

/* 卡片与标题 */
.login-card {
  width: min(440px, 94vw);
}

.card-header {
  font-size: 18px;
  font-weight: 600;
}

/* 表单布局 */
.form :deep(.el-form-item) {
  margin-bottom: 14px;
}

.submit-btn {
  width: 100%;
  margin-top: 6px;
}

.links {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}
</style>
