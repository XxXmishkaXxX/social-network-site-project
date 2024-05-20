<template>
  <div class="menu-item" @click="isOpen = !isOpen" >
        <a href ='#'>
            
        </a>
        <svg viewBox="0 0 1030 638" width="10">
            <path d="M1017 68L541 626q-11 12-26 12t-26-12L13 68Q-3 49 6 24.5T39 0h952q24 0 33 24.5t-7 43.5z" fill="#FFF"></path>
        </svg>
        <transition name="fade" apear>
         <div class="sub-menu" v-if="isOpen">
            <div class="menu-item">
              <router-link to="/services/web">Web</router-link>
            </div>
            <div class="menu-item">
              <router-link to="/services/design">Design</router-link>
            </div>
            <div class="menu-item">
              <router-link to="/services/videos">Videos</router-link>
            </div>
        </div>
        </transition>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      isOpen: false,
      isSubMenuOpen: false,
      isLoggedIn: false, // Предположим, что это состояние приходит из вашего хранилища состояний
      userProfile: {
        id: 1, // Замените на ID пользователя, если он доступен
        fullName: 'Имя пользователя', // Замените на имя пользователя, если оно доступно
        avatar: 'https://example.com/avatar.jpg' // Замените на URL аватара пользователя, если он доступен
      }
    };
  },
  methods: {
    checkToken() {
      const token = localStorage.getItem('token');
      this.isLoggedIn = !!token;
    },
    logout() {
      const token = localStorage.getItem('token');
      axios.post('http://127.0.0.1:8000/api/users/logout/', {}, {
        headers: {
          Authorization: `token ${token}`
        }
      })
      .then(() => {
        localStorage.removeItem('token')
      })
      .catch(error => {
        console.error('Ошибка при выходе:', error);
        // Обработка ошибки, если запрос на выход не удался
      });
    },
    redirectToLogin() {
      this.$router.push({ name: 'Login' });
    }
  },
  created() {
    this.checkToken();
  }
};
</script>

<style scoped>

</style>
