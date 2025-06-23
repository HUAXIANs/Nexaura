<template>
  <div id="app-container">
    <header class="app-header">
      <nav class="main-nav">
        <router-link to="/" class="nav-logo">NexAura</router-link>
        <div class="nav-links">
          <template v-if="isAuthenticated">
            <router-link to="/dashboard">{{ $t('nav.dashboard') }}</router-link>
            <router-link to="/profile">{{ $t('nav.profile') }}</router-link>
            <a href="#" @click.prevent="handleLogout">{{ $t('nav.logout') }}</a>
          </template>
          <template v-else>
            <router-link to="/">{{ $t('nav.home') }}</router-link>
            <router-link to="/login">{{ $t('nav.login') }}</router-link>
          </template>
        </div>
      </nav>
    </header>
    <main class="app-content">
      <router-view />
    </main>
    <footer class="app-footer">
      <p>&copy; 2024 NexAura. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
import { mapState, mapActions } from 'pinia';
import { useAuthStore } from './stores/auth';

export default {
  name: 'App',
  computed: {
    ...mapState(useAuthStore, ['isAuthenticated']),
  },
  methods: {
    ...mapActions(useAuthStore, ['logout']),
    handleLogout() {
      this.logout();
    }
  }
};
</script>

<style>
/* General App Styles */
#app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f7fafc;
}

.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 0 2rem;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.main-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
}

.nav-logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  text-decoration: none;
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

.app-content {
  flex-grow: 1;
  padding: 2rem;
  max-width: 1280px;
  width: 100%;
  margin: 0 auto;
}

.app-footer {
  text-align: center;
  padding: 1.5rem;
  color: #a0aec0;
  font-size: 0.875rem;
  background-color: #ffffff;
  border-top: 1px solid #e2e8f0;
}
</style>

