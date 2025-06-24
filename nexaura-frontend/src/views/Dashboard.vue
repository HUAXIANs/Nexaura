<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>{{ $t('dashboard.title') }}</h1>
      <p>{{ $t('dashboard.welcome') }}</p>
    </header>
    
    <!-- 項目管理區域 -->
    <div class="projects-section">
      <div class="projects-header">
        <h2>{{ $t('dashboard.my_projects') }}</h2>
        <button class="btn btn-primary" @click="showCreateProject = true">{{ $t('dashboard.button_new_project') }}</button>
      </div>
      
      <div class="projects-grid" v-if="projects.length > 0">
        <div 
          v-for="project in projects" 
          :key="project.id" 
          class="project-card"
          @click="selectProject(project)"
        >
          <button class="delete-project-btn" @click.stop="confirmDeleteProject(project.id)">
            &times;
          </button>
          <h3>{{ project.name }}</h3>
          <p>{{ project.description }}</p>
          <div class="card-footer">
            <span>{{ formatDate(project.created_at) }}</span>
          </div>
        </div>
      </div>
      
      <div v-else class="empty-state">
        <p>{{ $t('dashboard.empty_state_message') }}</p>
        <button @click="showCreateProject = true" class="btn btn-primary">
          {{ $t('dashboard.button_create_first_project') }}
        </button>
      </div>
    </div>
    
    <!-- 創作區域 -->
    <div v-if="selectedProject" class="creation-section">
      <div class="creation-card">
        <h2>{{ selectedProject.name }} - {{ $t('creation.title_suffix') }}</h2>
        <form @submit.prevent="handleGenerate">
          <div class="form-group">
            <label for="creation-topic">{{ $t('creation.topic') }}</label>
            <textarea 
              id="creation-topic" 
              v-model="creationTopic" 
              :placeholder="$t('creation.topic_placeholder')"
              rows="4"
              required
            ></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="target-platform">{{ $t('creation.target_platform') }}</label>
              <select id="target-platform" v-model="targetPlatform">
                <option value="xiaohongshu">小红书</option>
              </select>
            </div>
            <div class="form-group">
              <label for="content-style">{{ $t('creation.style') }}</label>
              <select id="content-style" v-model="contentStyle">
                <option value="explore">{{ $t('creation.style_option_explore') }}</option>
              </select>
            </div>
          </div>
          <div class="creation-actions">
            <button type="submit" class="btn btn-generate" :disabled="isGenerating">
              <i v-if="isGenerating" class="fas fa-spinner fa-spin"></i>
              {{ isGenerating ? '生成中...' : $t('creation.button_generate') }}
            </button>
          </div>
        </form>
      </div>
      
      <!-- 生成結果展示 -->
      <div v-if="generatedContent" class="result-section">
        <h3>{{ $t('creation.result_title') }}</h3>
        <div class="content-preview">
          <div class="content-title">
            <h4>{{ generatedContent.title }}</h4>
          </div>
          
          <div class="content-body">
            <p class="formatted-content">{{ generatedContent.content }}</p>
          </div>
          
          <div class="content-tags">
            <span v-for="tag in generatedContent.tags" :key="tag" class="tag">
              #{{ tag }}
            </span>
          </div>
          
          <div v-if="generatedContent.imageDescriptions" class="image-suggestions">
            <h5>{{ $t('creation.image_suggestions_title') }}</h5>
            <ul>
              <li v-for="(desc, index) in generatedContent.imageDescriptions" :key="index">
                {{ desc }}
              </li>
            </ul>
          </div>
        </div>
        
        <div class="result-actions">
          <button class="btn btn-secondary">{{ $t('creation.button_edit_content') }}</button>
          <button class="btn btn-primary">{{ $t('creation.button_save_project') }}</button>
          <button class="btn btn-success">{{ $t('creation.button_export_content') }}</button>
        </div>
      </div>
    </div>
    
    <!-- 新建項目模態框 -->
    <div v-if="showCreateProject" class="modal-overlay" @click="showCreateProject = false">
      <div class="modal-content" @click.stop>
        <h3>{{ $t('create_project_modal.title') }}</h3>
        <form @submit.prevent="createProject" class="project-form">
          <div class="form-group">
            <label for="project-name">{{ $t('create_project_modal.project_title_label') }}</label>
            <input 
              type="text" 
              id="project-name" 
              v-model="newProject.name" 
              required 
              :placeholder="$t('create_project_modal.project_title_placeholder')"
            />
          </div>
          
          <div class="form-group">
            <label for="project-desc">{{ $t('create_project_modal.project_desc_label') }}</label>
            <textarea 
              id="project-desc" 
              v-model="newProject.description" 
              :placeholder="$t('create_project_modal.project_desc_placeholder')"
              rows="3"
            ></textarea>
          </div>
          
          <div class="modal-actions">
            <button type="button" @click="showCreateProject = false" class="btn-cancel">{{ $t('create_project_modal.button_cancel') }}</button>
            <button type="submit" class="btn-confirm">{{ $t('create_project_modal.button_create') }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { supabase } from '../supabase'; // 导入 Supabase 客户端
import { useAuthStore } from '../stores/auth';
import axios from 'axios';
import { API_BASE_URL } from '../config';

// --- State Management ---
const projects = ref([]);
const selectedProject = ref(null);
const showCreateProject = ref(false);
const newProject = ref({ name: '', description: '' });
const creationTopic = ref('');
const targetPlatform = ref('xiaohongshu');
const contentStyle = ref('explore');
const generatedContent = ref(null);
const isGenerating = ref(false);
const isLoadingProjects = ref(true);

const authStore = useAuthStore();

// 创建一个经过认证的 axios 实例，用于调用后端业务逻辑 API
const createApiClient = () => {
  const token = authStore.session?.access_token;
  if (!token) {
    console.error("无法创建 API 客户端：用户未认证");
    return null;
  }
  return axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
};

// --- Lifecycle ---
onMounted(() => {
  fetchProjects();
});

// --- Methods ---
const fetchProjects = async () => {
  isLoadingProjects.value = true;
  try {
    const { data, error } = await supabase
      .from('projects')
      .select('*')
      .order('created_at', { ascending: false });

    if (error) throw error;
    
    projects.value = data;
    if (data && data.length > 0) {
      selectProject(data[0]);
    }
  } catch (error) {
    console.error('获取项目列表失败:', error.message);
  } finally {
    isLoadingProjects.value = false;
  }
};

const createProject = async () => {
  if (!newProject.value.name) {
    alert('项目标题不能为空');
    return;
  }
  try {
    const { data, error } = await supabase
      .from('projects')
      .insert({ 
        name: newProject.value.name,
        description: newProject.value.description,
        user_id: authStore.user.id
      })
      .select()
      .single();

    if (error) throw error;

    projects.value.unshift(data);
    selectProject(data);
    showCreateProject.value = false;
    newProject.value = { name: '', description: '' };
  } catch (error) {
    console.error('创建项目失败:', error.message);
  }
};

const confirmDeleteProject = async (projectId) => {
    if (confirm('您确定要删除这个项目吗？此操作不可撤销。')) {
        await deleteProject(projectId);
    }
};

const deleteProject = async (projectId) => {
    try {
        const { error } = await supabase
            .from('projects')
            .delete()
            .eq('id', projectId);

        if (error) throw error;

        // 从 UI 中移除项目
        projects.value = projects.value.filter(p => p.id !== projectId);
        if (selectedProject.value?.id === projectId) {
            selectedProject.value = projects.value.length > 0 ? projects.value[0] : null;
        }
    } catch (error) {
        console.error('删除项目失败:', error.message);
        alert('删除项目失败，请稍后重试。');
    }
};

const handleGenerate = async () => {
  isGenerating.value = true;
  generatedContent.value = null;
  const apiClient = createApiClient();
  if (!apiClient) return;

  const requestBody = {
    topic: creationTopic.value,
    platform: targetPlatform.value,
    style: contentStyle.value
  };

  try {
    const response = await apiClient.post('/content/generate', requestBody);
    generatedContent.value = response.data;
    if (generatedContent.value && generatedContent.value.content) {
      generatedContent.value.content = generatedContent.value.content.replace(/\\n/g, '<br>');
    }
  } catch (error) {
    console.error('生成内容失败:', error);
    alert(error.response?.data?.detail || error.message || '生成内容失败，请稍后重试');
  } finally {
    isGenerating.value = false;
  }
};

const selectProject = (project) => {
  selectedProject.value = project;
  generatedContent.value = null;
};

// --- Utility Functions ---
const isI18nKey = (text) => typeof text === 'string' && text.includes('.');
const formatDate = (dateString) => new Date(dateString).toLocaleDateString();

</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 2rem;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 3rem;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: #1e293b;
}

.dashboard-header p {
  font-size: 1.1rem;
  color: #64748b;
}

.projects-section {
  background-color: #ffffff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  margin-bottom: 2rem;
}

.projects-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.projects-header h2 {
  font-size: 1.5rem;
  color: #334155;
}

.btn, .btn-primary, .btn-secondary, .btn-generate, .btn-cancel, .btn-confirm {
    padding: 0.6rem 1.2rem;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.95rem;
    font-weight: 500;
    transition: all 0.2s ease-in-out;
}

.btn-primary, .btn-confirm {
  background: linear-gradient(90deg, #4F46E5, #818CF8);
  color: white;
}
.btn-primary:hover, .btn-confirm:hover {
  opacity: 0.9;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.project-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative; /* 为删除按钮定位 */
}

.delete-project-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: #f1f5f9;
  color: #64748b;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.2rem;
  line-height: 1;
  cursor: pointer;
  opacity: 0.6;
  transition: all 0.3s ease;
}

.project-card:hover .delete-project-btn {
  opacity: 1;
  background: #e2e8f0;
}

.delete-project-btn:hover {
  background: #ef4444;
  color: white;
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px rgba(0,0,0,0.07);
}

.project-card h3 {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: #1e293b;
}

.project-card p {
  color: #475569;
  font-size: 0.95rem;
  margin-bottom: 1rem;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
  color: #64748b;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  border: 2px dashed #e2e8f0;
  border-radius: 8px;
}

.empty-state p {
  margin-bottom: 1rem;
  color: #475569;
}

.btn-secondary {
    background-color: #e2e8f0;
    color: #1e293b;
}
.btn-secondary:hover {
    background-color: #cbd5e1;
}

/* Creation Section */
.creation-section {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
}
.creation-card {
  flex: 1;
  background-color: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.form-group {
    margin-bottom: 1.5rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #334155;
}

input[type="text"], textarea, select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    font-size: 1rem;
}

.form-row {
    display: flex;
    gap: 1rem;
}

.form-row .form-group {
    flex: 1;
}

.creation-actions {
    text-align: right;
}

.btn-generate {
    background: linear-gradient(90deg, #2563eb, #3b82f6);
    color: white;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2.5rem;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-cancel {
  background-color: #e2e8f0;
}

.btn-confirm {
  background-color: #2563eb;
  color: white;
}

/* Result Section */
.result-section {
  flex: 1;
  background-color: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.content-preview {
  background: #f7fafc;
  padding: 1.5rem;
  border-radius: 0.5rem;
  margin-bottom: 1.5rem;
}

.content-title h4 {
  color: #2d3748;
  font-size: 1.3rem;
  margin-bottom: 1rem;
}

.content-body {
  color: #4a5568;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.content-body p.formatted-content {
  white-space: pre-wrap;
  word-wrap: break-word;
  color: #333;
  line-height: 1.8;
  font-size: 0.95rem;
}

.content-tags {
  margin-top: 20px;
  margin-bottom: 1rem;
}

.tag {
  display: inline-block;
  background: #667eea;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.9rem;
  margin-right: 0.5rem;
  margin-bottom: 0.5rem;
}

.image-suggestions h5 {
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.image-suggestions ul {
  color: #718096;
  padding-left: 1.5rem;
}

.result-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn-success {
  background: #48bb78;
  color: white;
}

@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
  }
  
  .result-actions {
    flex-direction: column;
  }
  
  .projects-grid {
    grid-template-columns: 1fr;
  }
}
</style>

