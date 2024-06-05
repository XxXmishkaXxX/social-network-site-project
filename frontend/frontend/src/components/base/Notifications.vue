<template>
  <div class="notification-bell d-flex justify-content-between" ref="bellContainer">
    <i class="bi bi-bell-fill" @click="toggleNotifications"></i>
    <span v-if="unreadCount > 0" class="badge">{{ unreadCount }}</span>
    
    <notification-list 
      v-if="showNotifications" 
      :notifications="notifications" 
      @refresh-notifications="refreshNotifications"
    />
  </div>
</template>

<script>
import axios from 'axios';
import NotificationList from './NotificationsList.vue';
import { API_BASE_URL } from '@/config';

export default {
  components: {
    NotificationList,
  },
  data() {
    return {
      unreadCount: 0,
      notifications: [], 
      showNotifications: false, 
    };
  },
  methods: {
    connectWebSocket() {
      this.socket = new WebSocket(`ws://127.0.0.1:8000/ws/notifications/?token=${localStorage.getItem('token')}`);
      
      this.socket.onmessage = (event) => {
        let data = JSON.parse(event.data);
        if (data.type && !data.read) {
          this.unreadCount++;
          this.notifications.push(data);
        }
      };
      
      this.socket.onopen = () => {
        console.log('WebSocket connection established.');
      };
      
      this.socket.onclose = () => {
        console.log('WebSocket connection closed.');
      };
      
      this.socket.onerror = (error) => {
        console.log('WebSocket error:', error);
      };
    },
    toggleNotifications() {
      this.showNotifications = !this.showNotifications;
    },
    refreshNotifications() {

      this.getNotificationsList();
    },
    markAsRead() {
      this.unreadCount = 0;
    },
    async getNotificationsList() {
      try {
        const response = await axios.get(`${API_BASE_URL}/notifications/get-notifications/`, { 
          headers: {'Authorization': `token ${localStorage.getItem('token')}`}
        });
        this.notifications = response.data;
        this.unreadCount = response.data.filter(notification => !notification.read).length;
        console.log(this.notifications)
      } catch (error) {}
    }
  },
  mounted() {
    this.connectWebSocket();
    this.getNotificationsList();
  },
  beforeDestroy() {
    if (this.socket) {
      this.socket.close();
    }
  }
};
</script>

<style scoped>
@import url("../../styles/notifications/styles-notifications.css");
</style>
