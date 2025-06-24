<template>
  <div class="home-page">
    <NavBar />
    <div class="hero-section">
      <h1 class="hero-title">{{ t('hero.title') }}</h1>
      <p class="hero-subtitle">{{ t('hero.subtitle') }}</p>
      <p class="hero-description">{{ t('hero.description') }}</p>
      <div class="hero-actions">
        <router-link to="/login" class="btn btn-primary">{{ t('hero.button_create') }}</router-link>
        <button class="btn btn-secondary">{{ t('hero.button_learn_more') }}</button>
      </div>
    </div>
    
    <div class="features-section">
      <h2>{{ t('features.title') }}</h2>
      <div class="features-grid">
        <div class="feature-card">
          <h3>{{ t('features.card1_title') }}</h3>
          <p>{{ t('features.card1_desc') }}</p>
        </div>
        <div class="feature-card">
          <h3>{{ t('features.card2_title') }}</h3>
          <p>{{ t('features.card2_desc') }}</p>
        </div>
        <div class="feature-card">
          <h3>{{ t('features.card3_title') }}</h3>
          <p>{{ t('features.card3_desc') }}</p>
        </div>
        <div class="feature-card">
          <h3>{{ t('features.card4_title') }}</h3>
          <p>{{ t('features.card4_desc') }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import NavBar from '../components/NavBar.vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
</script>

<style scoped>
.home-page {
  background-color: #f7fafc;
}

.hero-section {
  text-align: center;
  padding: 5rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: rgba(255, 255, 255, 0.9);
}

.hero-description {
  font-size: 1.1rem;
  margin-bottom: 2.5rem;
  color: rgba(255, 255, 255, 0.8);
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn {
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.btn-primary {
  background-color: white;
  color: #667eea;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.btn-secondary {
  background-color: transparent;
  color: white;
  border-color: white;
}

.btn-secondary:hover {
  background: white;
  color: #667eea;
}

.features-section {
  padding: 4rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.features-section h2 {
  text-align: center;
  font-size: 2.5rem;
  color: #2d3748;
  margin-bottom: 3rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.feature-card h3 {
  font-size: 1.5rem;
  color: #2d3748;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #718096;
  line-height: 1.6;
}
</style>

