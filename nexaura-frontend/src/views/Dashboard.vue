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
          <h3>{{ isI18nKey(project.title) ? $t(project.title) : project.title }}</h3>
          <p>{{ isI18nKey(project.description) ? $t(project.description) : project.description }}</p>
          <div class="card-footer">
            <span>{{ formatDate(project.createdAt) }}</span>
            <span class="status" :class="project.status">{{ $t('project_card.status_' + project.status) }}</span>
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
        <h2>{{ isI18nKey(selectedProject.title) ? $t(selectedProject.title) : selectedProject.title }} - {{ $t('creation.title_suffix') }}</h2>
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
            <p v-html="generatedContent.content"></p>
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
            <label for="project-title">{{ $t('create_project_modal.project_title_label') }}</label>
            <input 
              type="text" 
              id="project-title" 
              v-model="newProject.title" 
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

<script>
import axios from 'axios';
import { API_ENDPOINTS, AUTH } from '../config';

export default {
  name: 'Dashboard',
  data() {
    return {
      projects: [
        {
          id: 1,
          title: 'dashboard.projects.p1.title',
          description: 'dashboard.projects.p1.description',
          createdAt: new Date('2024-01-15'),
          status: 'ongoing'
        }
      ],
      selectedProject: null,
      showCreateProject: false,
      newProject: {
        title: '',
        description: ''
      },
      creationTopic: '',
      targetPlatform: 'xiaohongshu',
      contentStyle: 'explore',
      generatedContent: null,
      isGenerating: false
    }
  },
  mounted() {
    // 组件挂载时，自动选择第一个项目
    if (this.projects.length > 0 && !this.selectedProject) {
      console.log('自动选择第一个项目');
      this.selectProject(this.projects[0]);
    }
  },
  methods: {
    isI18nKey(text) {
      return typeof text === 'string' && text.includes('.');
    },
    
    selectProject(project) {
      console.log('选择项目:', project);
      this.selectedProject = project;
      this.generatedContent = null;
    },
    
    createProject() {
      const project = {
        id: Date.now(),
        title: this.newProject.title,
        description: this.newProject.description,
        createdAt: new Date(),
        status: 'ongoing'  // 使用英文状态，与i18n保持一致
      }
      
      console.log('创建新项目:', project);
      this.projects.push(project);
      this.selectedProject = project;
      this.showCreateProject = false;
      
      // 清空表单
      this.newProject = {
        title: '',
        description: ''
      }
    },
    
    async handleGenerate() {
      this.isGenerating = true;
      this.generatedContent = null; // 开始生成时，清空之前的结果

      const requestBody = {
        topic: this.creationTopic,
        platform: this.targetPlatform,
        style: this.contentStyle
      };

      try {
        // 从localStorage获取token
        const token = localStorage.getItem(AUTH.TOKEN_KEY);
        
        // 使用配置文件中的API地址
        const apiUrl = API_ENDPOINTS.GENERATE_CONTENT;
        
        // 发起真实的API请求
        const response = await axios.post(apiUrl, requestBody, {
          headers: {
            'Authorization': token ? `Bearer ${token}` : '',
            'Content-Type': 'application/json'
          }
        });

        // 将返回的数据赋值给generatedContent
        this.generatedContent = response.data;
        
        // 处理内容显示
        if (this.generatedContent && this.generatedContent.content) {
          // 将换行符转换为<br>标签，以便正确显示
          this.generatedContent.content = this.generatedContent.content.replace(/\n\n/g, '<br><br>');
        }
        
      } catch (error) {
        console.error('生成内容失败:', error);
        // 向用户显示更友好的错误信息
        if (error.response) {
          const statusCode = error.response.status;
          if (statusCode === 401) {
            alert('请先登录后再尝试生成内容');
            this.$router.push('/login');
          } else if (statusCode === 400) {
            alert(`请求参数错误: ${error.response.data.detail || '请检查输入'}`);
          } else {
            alert(`生成失败: ${error.response.data.detail || '服务内部错误'}`);
          }
        } else if (error.request) {
          alert('无法连接到服务器，请检查网络连接或服务器是否运行');
        } else {
          alert('生成失败，请检查网络连接或联系管理员');
        }
      } finally {
        this.isGenerating = false;
      }
    },
    
    formatDate(date) {
      const localeMap = {
        'en': 'en-US',
        'zh-CN': 'zh-CN'
      };
      return date.toLocaleDateString(localeMap[this.$i18n.locale] || 'default');
    }
  }
}
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
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1.5rem;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
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

.content-tags {
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

