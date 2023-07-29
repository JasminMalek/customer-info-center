import { createApp } from 'vue';
import App from './App.vue';
import { routes } from './routes';
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

// Create Vue application instance
createApp(App)
  .use(router)
  .mount('#app');
