<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-brand">
        <h1>NEXAURA</h1>
        <p>{{ t('app.tagline') }}</p>
      </div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">{{ t('nav.home') }}</router-link>
        <router-link to="/login" class="nav-link">{{ t('nav.login') }}</router-link>
        <router-link to="/dashboard" class="nav-link">{{ t('nav.dashboard') }}</router-link>
        <select v-model="locale" class="lang-switcher">
          <option value="zh-CN">简体中文</option>
          <option value="en">English</option>
        </select>
      </div>
    </nav>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n';
const { t, locale } = useI18n();
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.nav-brand h1 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: bold;
}
.nav-brand p {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.9;
}
.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}
.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  transition: background-color 0.3s;
}
.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
}
.nav-link.router-link-active {
  background-color: rgba(255, 255, 255, 0.3);
}
.main-content {
  min-height: calc(100vh - 80px);
  padding: 2rem;
}
.lang-switcher {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 0.5rem;
  padding: 0.6rem;
  margin-left: 1rem;
  cursor: pointer;
  font-size: 0.9rem;
}
.lang-switcher:focus {
  outline: none;
}
.lang-switcher option {
  color: black;
  background-color: white;
}
</style>

