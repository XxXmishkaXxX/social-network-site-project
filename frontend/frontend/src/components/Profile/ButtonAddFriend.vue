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
  props: {
    isFriend: {
      type: Boolean,
      default: false
    },
    isRequestSentToUser: {
      type: Boolean,
      default: false
    },
    isRequestSentFromUser:{
      type: Boolean,
      default: false
    },
    userProfileId: {
      type: [String, Number],
      required: true
    }
  },
  computed: {
    buttonClass() {
      if (this.isFriend) {
        return 'friend btn';
      } else if (this.isRequestSentToUser) {
        return 'request-sent-to-user btn';
      } else if (this.isRequestSentFromUser){
          return 'request-sent-from-user btn'
      } 
      else{
        return 'not-friend btn';
      }
    },
    buttonText() {
      if (this.isFriend) {
        return 'В друзьях';
      } else if (this.isRequestSentToUser) {
        return 'Запрос отправлен';
      } else if(this.isRequestSentFromUser){
        return 'Принять запрос';
      } else {
        return 'Добавить в друзья';
      }
    }
  },
  methods: {
    async toggleFriendStatus() {
      try {
        if (this.isFriend) {
          await this.removeFriend();
          this.$emit('update:isFriend', false);
        } else if (this.isRequestSentToUser) {
          await this.cancelFriendRequest();
          this.$emit('update:isRequestSentToUser', false);
        } else if (this.isRequestSentFromUser){
          await this.acceptFriendRequest();
          this.$emit('update:isRequestSentFromUser', false);
        }
          else {
          await this.addFriend();
          this.$emit('update:isRequestSentToUser', true);
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
    async acceptFriendRequest() {
            try {
                await axios.put(`${API_BASE_URL}/relations/accept-friend-request/`, null, {
                    headers: {
                        'Authorization': `token ${localStorage.getItem('token')}`
                    },
                    params:{
                        from_user: this.userProfileId
                    }
                });

                this.users = this.users.filter(user => user.from_user !== userId);
            } catch (error) {
                console.error('Error accepting friend request:', error);
            }
        },

    async cancelFriendRequest() {
      try {
        const token = localStorage.getItem('token');
        await axios.delete(`${API_BASE_URL}/relations/cancel-friend-request/`,
          { headers: { Authorization: `token ${token}` },
            params: { to_user: this.userProfileId }}
        );
      } catch (error) {
        console.error('Error canceling friend request:', error);
        throw error;
      }
    },
    async removeFriend() {
      try {
        const token = localStorage.getItem('token');
        await axios.delete(`${API_BASE_URL}/relations/remove-friend/${this.userProfileId}/${this.$root.userId}/`,
          { headers: { Authorization: `token ${token}` } }
        );
      } catch (error) {
        console.error('Error removing friend:', error);
        throw error;
      }
    }
  },
  created() {
    console.log(this.userProfileId, this.isFriend, this.isRequestSentToUser, this.isRequestSentFromUser);
  }
};
</script>

<style scoped>
.friend {
  background-color: green;
  color: white;
}

.request-sent-to-user {
  background-color: rgb(37, 118, 224);
  color: white;
}

.request-sent-from-user {
  background-color: rgb(44, 224, 104);
  color: white;
}

.not-friend {
  background-color: rgb(123, 68, 253);
  color: white;
}
</style>
