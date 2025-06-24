import { defineStore } from 'pinia';
import { supabase } from '../supabase';

let resolveInitialization;
const initializationComplete = new Promise(resolve => {
  resolveInitialization = resolve;
});

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    session: null,
    profile: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.user,
    currentUser: (state) => state.profile,
    initializationComplete: () => initializationComplete,
  },
  actions: {
    async _fetchUserProfile() {
      if (!this.user) {
        this.profile = null;
        return;
      }
      try {
        const { data, error } = await supabase
          .from('user_profiles')
          .select('*')
          .eq('user_id', this.user.id)
          .single();

        if (error) {
          console.error('获取用户 Profile 失败:', error.message);
          this.profile = null;
        } else {
          this.profile = data;
        }
      } catch (e) {
        console.error('获取用户 Profile 时发生未知错误:', e.message);
        this.profile = null;
      }
    },

    initialize() {
      supabase.auth.onAuthStateChange(async (event, session) => {
        this.user = session?.user || null;
        this.session = session;
        
        await this._fetchUserProfile();

        if (resolveInitialization) {
          resolveInitialization();
          resolveInitialization = null; 
        }
      });
    },

    async logout() {
      const { error } = await supabase.auth.signOut();
      if (error) {
        console.error('Logout failed:', error.message);
      }
    },

    async register(userInfo) {
      const { email, password, username } = userInfo;
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: {
            username: username,
          },
        },
      });
      if (error) throw error;
      return data;
    },

    async login(credentials) {
      const { email, password } = credentials;
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });
      if (error) throw error;
      return data;
    },
  },
}); 