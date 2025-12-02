import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

// 路由表
const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        redirect: '/aifs/login',  // 根路径重定向到登录页
    },
    {
        path: '/aifs/login',
        name: 'Login',
        component: () => import('../views/Login.vue'),
        meta: { title: '登录' },
    },
    {
        path: '/aifs/register',
        name: 'Register',
        component: () => import('../views/Register.vue'),
        meta: { title: '注册' },
    },
    {
        path: '/aifs/chat',
        name: 'Chat',
        component: () => import('../views/chat.vue'),
        meta: { title: '聊天' },
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.afterEach((to) => {
    if (to.meta?.title) {
        document.title = String(to.meta.title)
    }
})

export default router