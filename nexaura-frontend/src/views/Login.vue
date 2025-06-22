<template>
  <div class="login-container">
    <div class="login-card">
      <h2>{{ $t('login.title') }}</h2>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">{{ $t('login.email') }}</label>
          <input 
            type="email" 
            id="email" 
            v-model="loginForm.email" 
            required 
          >
        </div>
        
        <div class="form-group">
          <label for="password">{{ $t('login.password') }}</label>
          <input 
            type="password" 
            id="password" 
            v-model="loginForm.password" 
            required 
          >
        </div>
        
        <button type="submit" class="login-btn" :disabled="isLoading">
          {{ isLoading ? '登錄中...' : $t('login.button_login') }}
        </button>
      </form>
      
      <div class="login-footer">
        <p>{{ $t('login.prompt_register') }} <a href="#" @click="showRegister = true">{{ $t('login.button_register_now') }}</a></p>
      </div>
    </div>
    
    <!-- 註冊彈窗 -->
    <div v-if="showRegister" class="modal-overlay" @click="showRegister = false">
      <div class="modal-content" @click.stop>
        <h3>{{ $t('register.title') }}</h3>
        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-group">
            <label for="reg-username">{{ $t('register.username') }}</label>
            <input 
              type="text" 
              id="reg-username" 
              v-model="registerForm.username" 
              required 
            >
          </div>
          <div class="form-group">
            <label for="reg-email">{{ $t('login.email') }}</label>
            <input 
              type="email" 
              id="reg-email" 
              v-model="registerForm.email" 
              :placeholder="$t('register.email_placeholder')"
              required 
            >
          </div>
          <div class="form-group">
            <label for="reg-password">{{ $t('login.password') }}</label>
            <input 
              type="password" 
              id="reg-password" 
              v-model="registerForm.password" 
              required 
            >
          </div>
          <div class="modal-actions">
            <button type="button" @click="showRegister = false" class="btn-cancel">{{ $t('register.button_cancel') }}</button>
            <button type="submit" class="btn-confirm">{{ $t('register.button_register') }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      loginForm: {
        email: '',
        password: ''
      },
      registerForm: {
        username: '',
        email: '',
        password: ''
      },
      isLoading: false,
      showRegister: false
    }
  },
  methods: {
    async handleLogin() {
      this.isLoading = true;
      try {
        // TODO: 實現登錄邏輯
        console.log('登錄信息:', this.loginForm);
        
        // 模擬 API 調用
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // 登錄成功後跳轉到工作台
        this.$router.push('/dashboard');
      } catch (error) {
        console.error('登錄失敗:', error);
        alert('登錄失敗，請檢查您的郵箱和密碼');
      } finally {
        this.isLoading = false;
      }
    },
    async handleRegister() {
      try {
        // TODO: 實現註冊邏輯
        console.log('註冊信息:', this.registerForm);
        
        // 模擬 API 調用
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        alert('註冊成功！請登錄');
        this.showRegister = false;
        
        // 清空註冊表單
        this.registerForm.username = '';
        this.registerForm.email = '';
        this.registerForm.password = '';
      } catch (error) {
        console.error('註冊失敗:', error);
        alert('註冊失敗，請稍後重試');
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-card h2 {
  text-align: center;
  color: #2d3748;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #4a5568;
  font-weight: 600;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
}

.login-btn {
  width: 100%;
  padding: 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-footer {
  text-align: center;
  margin-top: 1.5rem;
}

.login-footer a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.login-footer a:hover {
  text-decoration: underline;
}

/* 模態框樣式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  width: 90%;
  max-width: 400px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-content h3 {
  text-align: center;
  color: #2d3748;
  margin-bottom: 1.5rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-cancel, .btn-confirm {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-cancel {
  background: #e2e8f0;
  color: #4a5568;
}

.btn-cancel:hover {
  background: #cbd5e0;
}

.btn-confirm {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-confirm:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}
</style>

