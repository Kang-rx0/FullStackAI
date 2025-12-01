<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { registerAPI } from '@/api/user'

interface RegisterForm {
    username: string
    email: string
    password: string
    confirmPassword: string
}

const router = useRouter()
// 初始化表单，并把表单对象的节点设置为FormInstance类型
const formRef = ref<FormInstance>()

// 表单数据
const loading = ref(false)

// 定义表单的数据
const form = reactive<RegisterForm>({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
})

const rules: FormRules<RegisterForm> = {
    username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 2, max: 20, message: '用户名长度在 2 到 20 个字符', trigger: 'blur' }
    ],
    email: [
        { required: false, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
    ],
    password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度至少 6 个字符', trigger: 'blur' }
    ],
    confirmPassword: [
        { required: true, message: '请确认密码', trigger: 'blur' },
        {
            validator: (_rule, value, callback) => {
                if (value !== form.password) {
                    callback(new Error('两次输入的密码不一致'))
                } else {
                    callback()
                }
            },
            trigger: 'blur'
        }
    ]
}

const onSubmit = async() =>{
    // 确保表单有值
    if (!formRef.value) return

    // 校验表单
    await formRef.value.validate(async (valid) => {
        if (!valid) return // 校验失败，提前返回
        
        // 如果校验成功，设置 loading 状态
        loading.value = true

        try {
            // 调用后端注册接口 POST /aifs/register
            const response = await registerAPI({
                username: form.username,
                email: form.email,
                password: form.password,
                confirmPassword: form.confirmPassword,
            })

            // 注册成功
            ElMessage.success(response.message || '注册成功，请登录')

            // 存储用户信息到 localStorage（后续可改为 pinia store）
            // 这里不存储token，因为要让用户返回到登录页面登录
            localStorage.setItem('user', JSON.stringify(response.user))

            // 跳转到登录页面
            router.push('/aifs/login')
        } catch (error:any) {
            // 注册失败的错误信息
            ElMessage.error(error.message || '注册失败，请重试')
            console.error('注册失败：', error)
        } finally {
            loading.value = false
        }

    })

}
</script>

<template>
    <div class="register-page">
        <el-card class="register-card" shadow="hover">
            <template #header>
                <div class="card-header">注册</div>
            </template>

            <el-form
                ref="formRef"
                :model="form"
                :rules="rules"
                label-position="top"
                class="register-form"
            >
                <!-- UserName-->
                <el-form-item label = "用户名" prop="username">
                    <el-input v-model="form.username" placeholder ="请输入用户名"></el-input>
                </el-form-item>

                <!--Email-->
                <el-form-item label="邮箱" prop="email">
                    <el-input v-model="form.email" placeholder="输入邮箱"></el-input>
                </el-form-item>

                <!-- Password -->
                <el-form-item label="密码" prop="password">
                    <el-input 
                        v-model="form.password" 
                        type="password"
                        show-password
                        placeholder="输入密码"
                    ></el-input>
                </el-form-item>

                <!-- Confirm Password -->
                 <el-form-item label="确认密码" prop="confirmPassword">
                    <el-input 
                        v-model="form.confirmPassword" 
                        type="password"
                        show-password
                        placeholder="再次输入密码"
                    ></el-input>
                 </el-form-item>

                <!-- Submit Botton-->
                <el-button type="primary" class="submit-btn" @click="onSubmit">注册</el-button>
                
                <!-- Return to login-->
                <div class="return-login">
                    已有账号？
                    <el-link type="primary" @click="router.push('/aifs/login')">
                        返回登录
                    </el-link>
                </div>
            </el-form>
        </el-card>
    </div>

</template>

<style scoped>
/* 整页居中背景 */
.register-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: radial-gradient(ellipse at top, #f6faff 0%, #eef3fb 60%, #e8eef9 100%);
  padding: 16px;
}

/* 卡片与标题 */
.register-card {
  width: min(440px, 94vw);
}

.card-header {
  font-size: 18px;
  font-weight: 600;
}

/* 表单布局 */
.register-form :deep(.el-form-item) {
  margin-bottom: 14px;
}

.submit-btn {
  width: 100%;
  margin-top: 6px;
}

.return-login {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}
</style>
