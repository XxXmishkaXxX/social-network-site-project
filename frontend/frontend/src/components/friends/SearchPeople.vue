<template>
    <div>
      <div class="container d-flex flex-column align-items-center mt-5">
        <input class="form-control w-50 mb-3" type="text" v-model="searchQuery" @input="fetchUserProfiles" placeholder="Введите имя">
        <div class="w-100">
          <ul v-if="userProfiles.length > 0" class="list-group">
            <li v-for="user in userProfiles" :key="user.id" class="list-group-item d-flex justify-content-between align-items-center">
                    <div class="d-flex align-items-center">
                        <img :src="user.avatar" alt="avatar" class="rounded-circle me-3" width="50" height="50">
                        <div>
                            <h5 class="mb-0">
                                <a :href="`/wall/${user.user}/`" class="user-name">{{ user.full_name }}</a>
                            </h5>
                        </div>
                    </div>
                    <ButtonAddFriend
                    v-if="user.user && user.is_friend !== undefined"
                    :userProfileId="user.user"
                    :isFriend="user.is_friend.is_friend"
                    :isRequestSentToUser="user.is_friend.is_request_sent_to_user"
                    :isRequestSentFromUser="user.is_friend.is_request_sent_from_user"
                    @update:isFriend="(newValue) => handleUpdateIsFriend(newValue, user)"
                    @update:isRequestSentToUser="(newValue) => handleUpdateIsRequestSentToUser(newValue, user)"
                    @update:isRequestSentFromUser="(newValue) => handleUpdateIsRequestSentFromUser(newValue, user)"
                  />
                </li>
          </ul>
          <p v-else class="text-center mt-3">Нет профилей</p>
        </div>

      </div>
    </div>
  </template>
  
  
  <script>
  import axios from 'axios';
  import { API_BASE_URL } from '../../config';
  import ButtonAddFriend from '../Profile/ButtonAddFriend.vue';
  
  export default {
    components: {
        ButtonAddFriend
    },

    data() {
      return {
        searchQuery: '',
        userProfiles: []
      };
    },

    methods: {
    
      handleUpdateIsFriend(newValue, user) {
      user.is_friend.is_friend = newValue;
      },
      handleUpdateIsRequestSentToUser(newValue, user) {
        user.is_friend.is_request_sent_to_user = newValue;
      },

      handleUpdateIsRequestSentFromUser(newValue, user){
       user.is_friend.is_request_sent_from_user = newValue;
       user.is_friend.is_friend = true
      },
    async fetchUserProfiles() {
        if (this.searchQuery.trim().length <= 3) {
            this.userProfiles = [];
            return;
        }
      const config = {
        headers: {
          Authorization: `Token ${localStorage.getItem("token")}`
        },
        params: {
          search: this.searchQuery
        }
      };
      try {
        const response = await axios.get(`${API_BASE_URL}/profile/search/`, config);
        this.userProfiles = response.data;
      } catch (error) {
        console.error('Error fetching user profiles', error);
      }
    },
    isDifferentUser(userId) {
      const currentUserId = localStorage.getItem('UserID');
      return userId != currentUserId;
    }
  }
  }
  </script>
  
  <style scoped>
  .user-name {
    color: inherit;
    text-decoration: none;
    }
    .list-group-item {
        border: none;
        padding: 15px 20px;
        margin-bottom: 10px;
        background-color: #f8f9fa;
        border-radius: 8px;
    }
  </style>
  