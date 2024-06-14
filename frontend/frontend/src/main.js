import { createApp } from 'vue';
import App from './App.vue';
import router from './router';


import 'bootstrap/dist/css/bootstrap.css';

import 'bootstrap/dist/js/bootstrap.bundle.js';

import 'bootstrap-icons/font/bootstrap-icons.css';

const app = createApp(App);

import Notifications from './components/base/Notifications.vue';
app.component('Notifications', Notifications);

app.use(router);

app.mount('#app');
