<template>
  <div>
    <button :class="buttonClass" @click="toggleFollow">
      {{ isFollowing ? 'Отписаться' : 'Подписаться' }}
    </button>
  </div>
</template>

<script>
import axios from 'axios';
import { API_BASE_URL } from '../../config';

export default {

  props: {
    isFollowing: {
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
      return this.isFollowing ? 'btn btn-danger' : 'btn btn-primary';
    },
    buttonText() {
      return this.isFollowing ? 'Отписаться' : 'Подписаться';
    }
  },
  methods: {
    toggleFollow() {
      const endpoint = this.isFollowing ? 'unfollow/' : 'follow/';
      const config = {
        headers: {
          Authorization: `token ${localStorage.getItem("token")}`
        }
      };
      const data = {
        user_id: this.userProfileId // assuming userProfileId is correctly passed
      };

      axios.post(`${API_BASE_URL}/relations/${endpoint}`, data, config)
        .then(response => {
          // Update isFollowing state after successful request
          this.$emit('update:isFollowing', !this.isFollowing);
          // Additional actions after subscription change if needed
        })
        .catch(error => {
          console.error('Error toggling follow:', error);
          // Handle errors if necessary
        });
    }
  }
};
</script>

<style scoped>
/* Scoped styles for the button can be added here if needed */
</style>
