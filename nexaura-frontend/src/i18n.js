import { createI18n } from 'vue-i18n';
import en from './locales/en.json';
import zhCN from './locales/zh-CN.json';

const i18n = createI18n({
  legacy: false, // 必须为 false，才能在 setup 中使用 useI18n
  locale: 'zh-CN', // 默认语言
  fallbackLocale: 'en', // 回退语言
  messages: {
    'en': en,
    'zh-CN': zhCN,
  },
  globalInjection: true, // 可选，为了像 legacy:true 那样在模板里使用 $t
});

export default i18n; 