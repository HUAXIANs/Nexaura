<template>
  <div class="register-page">
    <NavBar />
    <div class="register-container">
      <div class="register-card">
        <h2>{{ t('register.title') }}</h2>
        <form @submit.prevent="handleRegister">
          <div class="input-group">
            <label for="username">{{ t('register.username') }}</label>
            <input type="text" id="username" v-model="username" required />
          </div>
          <div class="input-group">
            <label for="email">{{ t('login.email') }}</label>
            <input type="email" id="email" v-model="email" required />
          </div>
          <div class="input-group">
            <label for="password">{{ t('login.password') }}</label>
            <input type="password" id="password" v-model="password" required />
          </div>
          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
          <button type="submit" class="btn-register" :disabled="isLoading">
            {{ isLoading ? '注册中...' : t('register.button_register') }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import NavBar from '../components/NavBar.vue';

const username = ref('');
const email = ref('');
const password = ref('');
const errorMessage = ref('');
const isLoading = ref(false);

const authStore = useAuthStore();
const router = useRouter();
const { t } = useI18n();

const handleRegister = async () => {
  if (!username.value.trim()) {
    errorMessage.value = '用户名不能为空';
    return;
  }
  isLoading.value = true;
  errorMessage.value = '';
  try {
    await authStore.register({
      username: username.value,
      email: email.value,
      password: password.value,
    });
    router.push({ name: 'Login', query: { from: 'register' } });
  } catch (error) {
    errorMessage.value = error.message || '注册时发生未知错误';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.register-page {
  background-color: #f7fafc;
  min-height: 100vh;
}
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 4rem 2rem;
}
.register-card {
  width: 100%;
  max-width: 450px;
  background: white;
  padding: 3rem;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}
.register-card h2 {
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
.btn-register {
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
.btn-register:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style> 