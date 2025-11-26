import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

// 路由表：目前仅有登录页
const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'Login',
        component: () => import('../views/Login.vue'), // 懒加载登录页
        meta: { title: '登录' },
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