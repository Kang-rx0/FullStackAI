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
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

const pinia = createPinia()
// 注册持久化插件
pinia.use(piniaPluginPersistedstate)
app.use(pinia)

// 使用 Element Plus，并设置中文
app.use(ElementPlus, { locale: zhCn })

// mount app
app.mount('#app')
