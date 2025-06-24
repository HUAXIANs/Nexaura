import { createApp, ref } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import i18n from './i18n'
import './style.css'
import { useAuthStore } from './stores/auth'

// 创建一个全局响应式引用来跟踪错误状态
export const appCrashed = ref(false);

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)

// 设置全局错误处理器
app.config.errorHandler = (err, instance, info) => {
  // 发生任何未捕获的错误时，设置标志位
  appCrashed.value = true;
  
  // 在控制台打印详细错误，方便调试
  console.error("Vue Global Error:", err);
  console.error("At component:", instance);
  console.error("Error info:", info);
};

const authStore = useAuthStore()

// 启动时检查认证状态 - 这行代码已被 App.vue 中的 initialize() 代替
// authStore.checkAuth()

app.use(router)
app.use(i18n)

app.mount('#app')

