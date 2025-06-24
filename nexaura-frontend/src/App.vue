<template>
  <ErrorDisplay v-if="appCrashed" />
  <router-view v-else />
</template>

<script setup>
import { onMounted } from 'vue';
import { useAuthStore } from './stores/auth';
import { appCrashed } from './main.js';
import ErrorDisplay from './components/ErrorDisplay.vue';

const authStore = useAuthStore();

onMounted(() => {
  authStore.initialize();
});
</script>

