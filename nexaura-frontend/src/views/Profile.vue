<template>
  <div class="profile-container">
    <div class="profile-card">
      <h2>{{ $t('profile.title') }}</h2>
      <div v-if="currentUser" class="profile-info">
        <div class="info-item">
          <strong>{{ $t('profile.username') }}:</strong>
          <span>{{ currentUser.username }}</span>
        </div>
        <div class="info-item">
          <strong>{{ $t('profile.email') }}:</strong>
          <span>{{ currentUser.email }}</span>
        </div>
        <div class="info-item">
          <strong>ID:</strong>
          <span>{{ currentUser.id }}</span>
        </div>
      </div>
      <div v-else>
        <p>{{ $t('profile.loading') }}</p>
      </div>
      <button @click="handleLogout" class="logout-btn">
        {{ $t('profile.logout') }}
      </button>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'pinia';
import { useAuthStore } from '../stores/auth';

export default {
  name: 'Profile',
  computed: {
    ...mapState(useAuthStore, ['currentUser']),
  },
  methods: {
    ...mapActions(useAuthStore, ['logout']),
    handleLogout() {
      this.logout();
    },
  },
};
</script>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.profile-card {
  background: white;
  padding: 2.5rem;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
  text-align: center;
}

.profile-card h2 {
  color: #2d3748;
  margin-bottom: 2rem;
}

.profile-info {
  text-align: left;
  margin-bottom: 2rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 1rem 0;
  border-bottom: 1px solid #e2e8f0;
}

.info-item:last-child {
  border-bottom: none;
}

.info-item strong {
  color: #4a5568;
  font-weight: 600;
}

.info-item span {
  color: #718096;
}

.logout-btn {
  background-color: #e53e3e;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-btn:hover {
  background-color: #c53030;
}
</style> 