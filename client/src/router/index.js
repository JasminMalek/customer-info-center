import { createApp } from 'vue';
import App from 'client/src/App.vue';
import VueAxios from 'vue-axios';
import axios from 'axios';
import { routes } from 'client/src/routes';
import { createRouter, createWebHistory } from 'vue-router';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

// Create Vue application instance
const app = createApp(App);

// Use VueAxios plugin (optional)
app.use(VueAxios, axios);

// Mount the Vue application instance to the DOM
app.use(router);
app.mount('#app');
