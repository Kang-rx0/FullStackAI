import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
// Element Plus 全量引入（含中文本地化）
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'

const app  = createApp(App)

// import router
import router from './router'
app.use(router)

// import pinia
import { createPinia } from 'pinia'
const pinia = createPinia()

// import use persist
import { usePersist } from 'pinia-use-persist'
// 先注册持久化插件，再挂载到应用
pinia.use(usePersist)
app.use(pinia as any)
// 使用 Element Plus，并设置中文（对 3.5 的插件类型做轻量断言）
app.use(ElementPlus as any, { locale: zhCn } as any)

// mount app
app.mount('#app')
