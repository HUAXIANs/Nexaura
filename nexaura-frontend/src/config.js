/**
 * 应用程序配置
 */

// API基础URL
export const API_BASE_URL = 'http://127.0.0.1:8000/api';

// API端点
export const API_ENDPOINTS = {
  // 认证相关
  LOGIN: `${API_BASE_URL}/auth/login`,
  REGISTER: `${API_BASE_URL}/auth/register`,
  
  // 内容生成相关
  GENERATE_CONTENT: `${API_BASE_URL}/content/generate`,
  GET_PLATFORMS: `${API_BASE_URL}/content/platforms`,
  GET_STYLES: `${API_BASE_URL}/content/styles`,
  
  // 项目管理相关
  PROJECTS: `${API_BASE_URL}/projects`,
};

// 认证相关
export const AUTH = {
  TOKEN_KEY: 'auth_token',
  USER_INFO_KEY: 'user_info',
};

export default {
  API_BASE_URL,
  API_ENDPOINTS,
  AUTH,
}; 