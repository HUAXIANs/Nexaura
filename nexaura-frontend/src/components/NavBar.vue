<template>
  <header class="app-header">
    <nav class="main-nav">
      <router-link to="/" class="nav-logo">NexAura</router-link>
      <div class="nav-right-section">
        <div class="nav-links">
          <template v-if="isAuthenticated">
            <router-link to="/dashboard">{{ t('nav.dashboard') }}</router-link>
            <router-link to="/profile">{{ t('nav.profile') }}</router-link>
            <a href="#" @click.prevent="handleLogout">{{ t('nav.logout') }}</a>
          </template>
          <template v-else>
            <router-link to="/">{{ t('nav.home') }}</router-link>
            <router-link to="/login">{{ t('nav.login') }}</router-link>
          </template>
        </div>

        <!-- Language Switcher Dropdown -->
        <div class="language-switcher">
          <button @click="toggleDropdown" class="switcher-button">
            <span>{{ currentLanguage.name }}</span>
            <svg class="dropdown-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          </button>
          <div v-if="isDropdownOpen" class="dropdown-menu">
            <a href="#" @click.prevent="switchLanguage('zh-CN')" class="dropdown-item">中文 (简体)</a>
            <a href="#" @click.prevent="switchLanguage('en')" class="dropdown-item">English</a>
          </div>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const { t, locale } = useI18n();
const router = useRouter();

const isAuthenticated = computed(() => authStore.isAuthenticated);
const isDropdownOpen = ref(false);

const languages = {
  'zh-CN': { name: '中文' },
  'en': { name: 'EN' },
};

const currentLanguage = computed(() => languages[locale.value] || languages['zh-CN']);

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};

const switchLanguage = (lang) => {
  locale.value = lang;
  isDropdownOpen.value = false;
};

const handleLogout = async () => {
  await authStore.logout();
  router.push('/login');
};
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 0 2rem; /* Provides space on the sides */
  position: sticky;
  top: 0;
  z-index: 1000;
  color: white;
}

.main-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
  width: 100%; /* Ensures the nav spans the full width */
}

.nav-logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  text-decoration: none;
}

.nav-right-section {
  display: flex;
  align-items: center;
}

.nav-links a {
  margin-left: 1.5rem;
  text-decoration: none;
  color: rgba(255, 255, 255, 0.85);
  font-weight: 500;
  transition: color 0.3s ease;
}

.nav-links a:hover,
.nav-links a.router-link-exact-active {
  color: white;
}

.language-switcher {
  position: relative;
  margin-left: 1.5rem;
}

.switcher-button {
  display: flex;
  align-items: center;
  background: transparent;
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.5);
  padding: 0.4rem 0.8rem;
  border-radius: 0.5rem;
  cursor: pointer;
}

.dropdown-icon {
  width: 1rem;
  height: 1rem;
  margin-left: 0.5rem;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
  overflow: hidden;
  min-width: 120px;
}

.dropdown-item {
  display: block;
  padding: 0.75rem 1rem;
  color: #333;
  text-decoration: none;
}

.dropdown-item:hover {
  background-color: #f0f0f0;
}
</style> 