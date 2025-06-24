<template>
  <div class="profile-container">
    <div class="profile-card">
      <h2>{{ t('profile.title') }}</h2>
      
      <div v-if="profile && user" class="profile-info">
        <div class="info-item">
          <strong>ID:</strong>
          <span>{{ profile.id }}</span>
        </div>
        <div class="info-item">
          <strong>{{ t('profile.username') }}:</strong>
          <span>{{ profile.username }}</span>
        </div>
        <div class="info-item">
          <strong>{{ t('profile.email') }}:</strong>
          <span>{{ user.email }}</span>
        </div>
      </div>

      <div v-else class="text-center">
        <p>{{ t('profile.loading') }}</p>
      </div>

      <button @click="handleLogout" class="logout-btn">
        {{ t('profile.logout') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const { t } = useI18n();
const router = useRouter();

const profile = computed(() => authStore.profile);
const user = computed(() => authStore.user);

const handleLogout = async () => {
  await authStore.logout();
  router.push('/login');
};
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
}

.profile-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.profile-card h2 {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 2rem;
  color: #333;
}

.profile-info {
  text-align: left;
  margin-bottom: 2rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 1rem 0;
  border-bottom: 1px solid #eee;
  font-size: 1.1rem;
}

.info-item:last-child {
  border-bottom: none;
}

.info-item strong {
  color: #555;
  margin-right: 1rem;
}

.info-item span {
  color: #333;
}

.logout-btn {
  width: 100%;
  padding: 0.8rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
  background-color: #e53e3e;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-btn:hover {
  background-color: #c53030;
}
</style> 