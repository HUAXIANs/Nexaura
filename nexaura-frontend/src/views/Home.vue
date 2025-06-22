<template>
  <div class="home">
    <div class="hero-section">
      <h1 class="hero-title">{{ t('hero.title') }}</h1>
      <p class="hero-subtitle">{{ t('hero.subtitle') }}</p>
      <p class="hero-description">
        {{ t('hero.description') }}
      </p>
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
import { useI18n } from 'vue-i18n';
const { t } = useI18n();
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  text-align: center;
  padding: 4rem 0;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 1rem;
  margin-bottom: 3rem;
}

.hero-title {
  font-size: 3rem;
  font-weight: bold;
  color: #2d3748;
  margin-bottom: 1rem;
}

.hero-subtitle {
  font-size: 1.5rem;
  color: #4a5568;
  margin-bottom: 1rem;
}

.hero-description {
  font-size: 1.1rem;
  color: #718096;
  margin-bottom: 2rem;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: transparent;
  color: #667eea;
  border: 2px solid #667eea;
}

.btn-secondary:hover {
  background: #667eea;
  color: white;
}

.features-section h2 {
  text-align: center;
  font-size: 2.5rem;
  color: #2d3748;
  margin-bottom: 2rem;
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
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
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

