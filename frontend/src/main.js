import { createApp } from 'vue'
import router from './router'
import App from './App.vue'
import axios from 'axios'

import 'aos/dist/aos.css';
import './css/style.css'

console.log(process.env.VUE_APP_BASE_URL)
const axiosInstance = axios.create({
  baseURL: process.env.NODE_ENV == 'development' ? 'http://127.0.0.1:8000' : 'https://luminal-production.up.railway.app',
});

const app = createApp(App)

app.config.globalProperties.$axios = axiosInstance;

app.use(router)
app.mount('#app')
