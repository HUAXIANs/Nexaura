import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Profile from '../views/Profile.vue'
import MainLayout from '../layouts/MainLayout.vue'
import { AUTH } from '../config'
import { useAuthStore } from '../stores/auth'
import Register from '../views/Register.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      guest: true
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: {
      guest: true
    }
  },
  {
    path: '/app',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      { path: '/dashboard', name: 'Dashboard', component: Dashboard },
      { path: '/profile', name: 'Profile', component: Profile }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 全局前置守卫
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  // 1. 等待认证状态初始化完成
  await authStore.initializationComplete;

  const isAuthenticated = authStore.isAuthenticated;
  const isGuestRoute = to.matched.some(record => record.meta.guest);
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

  if (isGuestRoute) {
    if (isAuthenticated) {
      // 如果已登录用户访问访客页面(如/login)，则直接跳转到工作台
      next({ name: 'Dashboard' });
    } else {
      // 如果未登录，则允许访问
      next();
    }
  } else if (requiresAuth) {
    if (isAuthenticated) {
      // 如果已登录，则允许访问需要认证的页面
      next();
    } else {
      // 如果未登录，则跳转到登录页
      next({ name: 'Login', query: { redirect: to.fullPath } });
    }
  } else {
    // 对于不需要特殊权限的页面，直接放行
    next();
  }
});

export default router

