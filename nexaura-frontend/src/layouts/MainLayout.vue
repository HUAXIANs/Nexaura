<template>
  <div class="app-container">
    <NavBar />

    <main class="app-content">
      <router-view />
    </main>

    <footer class="app-footer">
      <p>&copy; 2024 NexAura. All rights reserved.</p>
    </footer>
  </div>
</template>

<script setup>
import NavBar from '../components/NavBar.vue';
</script>

<style>
/* Keeping the global layout styles, but removing header-specific styles */
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f7fafc;
}

.app-content {
  flex-grow: 1;
  padding: 2rem;
  width: 100%;
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