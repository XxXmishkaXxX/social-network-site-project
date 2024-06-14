<template>
  <div class="menu-home-page">
    <div v-if="isAuthenticated">
      <div v-if="userProfile" class="d-flex align-items-center">
        <div class="d-flex align-items-center me-3">
          <img :src="userProfile.avatar" alt="Avatar" class="rounded-circle me-3" width="50" height="50">
          <span>{{ userProfile.full_name }}</span>
        </div>

        <div class="ms-minus-1" ref="dropdown">
          <button class="btn btn-profile" @click="toggleMenu">
            <i class="bi bi-three-dots"></i>
            
          </button>
          <div v-if="showMenu" class="dropdown-menu" style="position: absolute; right: 0; top: 100%;">
            <nav class="menu">
              <ul class="list-unstyled mt-3">
                <li class="nav-item">
                  <a class="nav-link px-4" :href="`/wall/${userProfile.pk}`">Профиль</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link px-4" href="/profile/edit/">Редактирование профиля</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link px-4" href="#">Поддержка</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link px-4" @click="logout">Выйти</a>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </div>
      <div v-else>
        <button class="btn btn-outline-dark" @click="redirectToCreateProfile">Создать профиль</button>
        <button class="btn btn-outline-dark ms-2" @click="logout">Выйти</button>
      </div>
    </div>
    <div v-else>
      <button class="btn btn-outline-dark" @click="redirectToLogin">Войти</button>
    </div>
  </div>
</template>

<script>
import { API_BASE_URL } from '../../config';
import axios from 'axios';

export default {
  data() {
    return {
      isAuthenticated: false,
      userProfile: null,
      showMenu: false
    };
  },
  created() {
    this.checkToken();
  },
  methods: {
    toggleMenu() {
      this.showMenu = !this.showMenu;
      if (this.showMenu) {
        document.addEventListener('click', this.closeMenuOnClickOutside);
      } else {
        document.removeEventListener('click', this.closeMenuOnClickOutside);
      }
    },
    closeMenuOnClickOutside(event) {
      if (this.$refs.dropdown && !this.$refs.dropdown.contains(event.target)) {
        this.showMenu = false;
        document.removeEventListener('click', this.closeMenuOnClickOutside);
      }
    },
    checkToken() {
      const token = localStorage.getItem('token');
      if (token) {
        this.isAuthenticated = true;
        this.getUserData(token);
      } else {
        this.isAuthenticated = false;
      }
    },
    getUserData(token) {
      const id = localStorage.getItem('UserID');
      axios.get(`${API_BASE_URL}/profile/short/${id}/`, {
        headers: {
          Authorization: `token ${token}`,
        },
      })
      .then(response => {
        this.userProfile = response.data;
      })
      .catch(error => {
        console.error('Ошибка при получении данных пользователя:', error);
      });
    },
    logout() {
      const token = localStorage.getItem('token');
      axios.post(`${API_BASE_URL}/users/logout/`, null, {
        headers: {
          Authorization: `token ${token}`,
        },
      })
      .then(() => {
        localStorage.removeItem('token');
        this.isAuthenticated = false;
        this.userProfile = null;
        this.$router.push({ name: 'Home' });
      })
      .catch(error => {
        console.error('Ошибка при выходе:', error);
      });
    },
    redirectToLogin() {
      this.$router.push({ name: 'Login' });
    },
    redirectToCreateProfile() {
      this.$router.push({ name: 'CreateProfile' });
    },
  },
};
</script>

<style scoped>
@import '../../styles/profile/burger-menu-profile.css';
</style>
