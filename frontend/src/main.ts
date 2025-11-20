import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

const app  = createApp(App);

// import router
import router from "./router";
app.use(router);

// import pinia
import { createPinia } from "pinia";
const pinia = createPinia();
app.use(pinia);

// import use persist
import {usePersist} from "pinia-use-persist";
pinia.use(usePersist);
app.use(pinia);

// mount app
app.mount('#app')
