import { defineStore } from 'pinia';
import axios from 'axios';
import { API_BASE_URL, API_ENDPOINTS, AUTH } from '../config';
import router from '../router';

// 创建一个 Axios 实例，用于后续的 API 请求
const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

// 添加请求拦截器
apiClient.interceptors.request.use(config => {
  const authStore = useAuthStore();
  const token = authStore.token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});


export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem(AUTH.TOKEN_KEY) || null,
    user: JSON.parse(localStorage.getItem(AUTH.USER_INFO_KEY)) || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user,
  },
  actions: {
    async login(credentials) {
      try {
        const response = await axios.post(API_ENDPOINTS.LOGIN, credentials);
        if (response.data && response.data.access_token) {
          this.token = response.data.access_token;
          this.user = response.data.user;

          localStorage.setItem(AUTH.TOKEN_KEY, this.token);
          localStorage.setItem(AUTH.USER_INFO_KEY, JSON.stringify(this.user));
          
          // 更新 apiClient 的 Authorization header
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;

          router.push('/dashboard');
        } else {
          throw new Error('登錄響應中沒有找到token');
        }
      } catch (error) {
        console.error('登录失败:', error);
        // 抛出错误，以便组件可以处理它
        throw error;
      }
    },
    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem(AUTH.TOKEN_KEY);
      localStorage.removeItem(AUTH.USER_INFO_KEY);
      // 移除 apiClient 的 Authorization header
      delete apiClient.defaults.headers.common['Authorization'];
      router.push('/login');
    },
    async checkAuth() {
        if (!this.token) {
            return;
        }
        try {
            // 通过调用受保护的端点来验证令牌
            const response = await apiClient.get('/auth/me');
            this.user = response.data;
            localStorage.setItem(AUTH.USER_INFO_KEY, JSON.stringify(this.user));
        } catch (error) {
            console.error('Token validation failed:', error);
            this.logout();
        }
    },
    async register(userInfo) {
      try {
        await axios.post(API_ENDPOINTS.REGISTER, userInfo);
      } catch (error) {
        console.error('注册失败:', error);
        throw error;
      }
    }
  },
});

// 导出配置好的 apiClient
export { apiClient }; 