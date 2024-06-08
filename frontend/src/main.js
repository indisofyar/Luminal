import { createApp } from 'vue'
import router from './router'
import App from './App.vue'
import axios from 'axios'

import 'aos/dist/aos.css';
import './css/style.css'

const axiosInstance = axios.create({
  baseURL: process.env.BASE_URL || 'https://luminal-production.up.railway.app',
});

const app = createApp(App)

app.config.globalProperties.$axios = axiosInstance;

app.use(router)
app.mount('#app')
