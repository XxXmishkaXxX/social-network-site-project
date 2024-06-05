import { createApp } from 'vue'
import App from './App.vue'
import router from './router'


import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle'
import 'bootstrap-icons/font/bootstrap-icons.css';

const app = createApp(App)

// Регистрация компонента уведомлений
import Notifications from './components/base/Notifications.vue'
app.component('Notifications', Notifications)

// Настройка подключения к серверу WebSocket
app.use(router)

app.mount('#app')
