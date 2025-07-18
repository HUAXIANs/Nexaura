<template>
  <div class="login-page">
    <NavBar />
    <div class="login-container">
      <div class="login-card">
        <div v-if="showVerificationMessage" class="verification-message">
          注册成功！请检查您的邮箱以完成账户验证，然后即可登录。
        </div>
        <h2>{{ t('login.title') }}</h2>
        <form @submit.prevent="handleLogin">
          <div class="input-group">
            <label for="email">{{ t('login.email') }}</label>
            <input type="email" id="email" v-model="email" required />
          </div>
          <div class="input-group">
            <label for="password">{{ t('login.password') }}</label>
            <input type="password" id="password" v-model="password" required />
          </div>
          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
          <button type="submit" class="btn-login" :disabled="isLoading">
            {{ isLoading ? '登录中...' : t('login.button_login') }}
          </button>
        </form>
        <div class="register-prompt">
          <p>{{ t('login.prompt_register') }} <router-link to="/register">{{ t('login.button_register_now') }}</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter, useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import NavBar from '../components/NavBar.vue';

const email = ref('');
const password = ref('');
const errorMessage = ref('');
const isLoading = ref(false);
const showVerificationMessage = ref(false);

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();
const { t } = useI18n();

onMounted(() => {
  if (route.query.from === 'register') {
    showVerificationMessage.value = true;
  }
});

const handleLogin = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    await authStore.login({
      email: email.value,
      password: password.value,
    });
    // 登录成功，立即跳转到工作台
    router.push({ name: 'Dashboard' });
  } catch (error) {
    errorMessage.value = error.message || '登录时发生未知错误';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.login-page {
  background-color: #f7fafc;
  min-height: 100vh;
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 4rem 2rem;
}

.login-card {
  width: 100%;
  max-width: 450px;
  background: white;
  padding: 3rem;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.login-card h2 {
  text-align: center;
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 2rem;
  color: #333;
}

.input-group {
  margin-bottom: 1.5rem;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #555;
}

.input-group input {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
  font-size: 1rem;
}

.error-message {
  color: #e53e3e;
  margin-bottom: 1rem;
  text-align: center;
}

.btn-login {
  width: 100%;
  padding: 0.8rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: opacity 0.3s ease;
}

.btn-login:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.register-prompt {
  text-align: center;
  margin-top: 1.5rem;
  color: #555;
}

.register-prompt a {
  color: #667eea;
  font-weight: 600;
  text-decoration: none;
}

.verification-message {
  padding: 1rem;
  margin-bottom: 1.5rem;
  background-color: #e6fffa;
  color: #2c7a7b;
  border-left: 4px solid #38b2ac;
  border-radius: 0.25rem;
  font-weight: 500;
}
</style>

