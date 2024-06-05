<template>
  <div class="notification-list">
    <!-- Показать кнопку "Очистить все" только если есть уведомления -->
    <button v-if="notifications.length > 0" @click="clearAll" class="btn btn-danger btn-sm">Очистить все</button>
    <!-- Если нет уведомлений, отобразить сообщение -->
    <div v-if="notifications.length === 0">Нет уведомлений</div>
      <!-- Вывести уведомления -->
      <div v-for="(notification, index) in notifications" :key="index" class="notification-item">
        <div class="notification-content">
          <img :src="notification.sender_avatar" alt="Avatar" class="avatar">
          <div class="me-2">
            <a :href="'/wall/' + notification.sender_id"><h6>{{ notification.sender_fullname }}</h6></a>
            <p>{{ notification.message }}</p>
          </div>
          <button @click="removeNotification(index)" class="btn btn-outline-danger btn-sm">X</button>
        </div>
      </div>
  </div>
</template>

<script>
import axios from 'axios';
import { API_BASE_URL } from '@/config';

export default {
  props: {
    notifications: {
      type: Array,
      default: () => []
    }
  },
  mounted() {
    this.markAsRead(); 
  },
  methods: {
    async markAsRead() {
      try {
        await axios.post(`${API_BASE_URL}/notifications/mark-as-read/`, null, {
          headers: {
            'Authorization': `token ${localStorage.getItem('token')}`
          }
        });
        this.$emit('refresh-notifications'); 
      } catch (error) {
        console.error("Error marking notifications as read:", error);
      }
    },
    async clearAll() {
      try {
        await axios.delete(`${API_BASE_URL}/notifications/delete-all/`, {
          headers: {
            'Authorization': `token ${localStorage.getItem('token')}`
          }
        });
        this.$emit('refresh-notifications');
      } catch (error) {
        console.error("Error clearing notifications:", error);
      }
    },
    async removeNotification(index) {
      try {
        await axios.delete(`${API_BASE_URL}/notifications/delete/${this.notifications[index].id}/`, {
          headers: {
            'Authorization': `token ${localStorage.getItem('token')}`
          }
        });
        this.notifications.splice(index, 1);
        this.$emit('refresh-notifications'); 
      } catch (error) {
        console.error("Error removing notification:", error);
      }
    }
  }
};
</script>

<style scoped>
@import url("../../styles/notifications/styles-notifications.css");
</style>

