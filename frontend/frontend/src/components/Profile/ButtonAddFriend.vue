<template>
    <button @click="toggleFriendStatus" :class="buttonClass">
      {{ buttonText }}
    </button>
  </template>
  
  <script>
  import axios from 'axios';
  import { API_BASE_URL } from '../../config';
  
  export default {
    name: 'AddFriendButton',
    props: ['userId'],
    data() {
      return {
        isFriend: null,
        isRequestSent: null,
        userProfileId: null,
      };
    },

    computed: {
    
      buttonClass() {
        if (this.isFriend) {
          return 'friend';
        } else if (this.isRequestSent) {
          return 'request-sent';
        } else {
          return 'not-friend';
        }
      },
      buttonText() {
        if (this.isFriend) {
          return 'В друзьях';
        } else if (this.isRequestSent) {
          return 'Запрос отправлен';
        } else {
          return 'Добавить в друзья';
        }
      }
    },
    methods: {
        async checkFriendStatus() {
      try {
        const token = localStorage.getItem('token');
        if (token) {
          const response = await axios.get(`${API_BASE_URL}/relations/check-friend-status/${this.userProfileId}/`, {
            headers: { Authorization: `token ${token}` }
          });
          this.isFriend = response.data.is_friend;
          this.isRequestSent = response.data.is_request_sent;
        }
      } catch (error) {
        console.error('Error checking friend status:', error);
      }
    },

      async toggleFriendStatus() {
        try {
          if (this.isFriend) {
            await this.removeFriend();
            this.isFriend = false;
          } else if (this.isRequestSent) {
            console.log('Запрос уже отправлен');
          } else {
            await this.addFriend();
            this.isRequestSent = true;
          }
        } catch (error) {
          console.error('Error toggling friend status:', error);
        }
      },
      async addFriend() {
        try {
          const token = localStorage.getItem('token');
          await axios.post(`${API_BASE_URL}/relations/send-friend-requests/`, 
            { to_user: this.userProfileId },
            { headers: { Authorization: `token ${token}` } }
          );
        } catch (error) {
          console.error('Error adding friend:', error);
          throw error;
        }
      },
      async removeFriend() {
        try {
          const token = localStorage.getItem('token');
          await axios.post(`${API_BASE_URL}/relations/remove-friend/`, 
            { to_user: this.userProfileId },
            { headers: { Authorization: `token ${token}` } }
          );
        } catch (error) {
          console.error('Error removing friend:', error);
          throw error;
        }
      }
    }, 
    created() {
        this.userProfileId = this.$route.params.UserID;
        this.checkFriendStatus();
    }
    };
  </script>
  
  <style scoped>
  .friend {
    background-color: green;
    color: white;
  }
  
  .request-sent {
    background-color: orange;
    color: white;
  }
  
  .not-friend {
    background-color: gray;
    color: white;
  }
  </style>
  