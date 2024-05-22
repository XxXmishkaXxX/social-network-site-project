<template>
  <div class="menu-home-page navbar-nav ms-auto logo-button">
    <div v-if="isAuthenticated">
      <div v-if="userProfile">
        <div>
          <img :src="userProfile.avatar" class="me-2" alt="Avatar"
               style="width: 50px; height: 50px; border-radius:50px; object-fit: cover;">
          {{ userProfile.full_name }}
        </div>
        <div class="menu ms-2">
          <button class="btn btn-profile">
            <i class="bi bi-list" style="width: 20px; height: 20px;"></i>
          </button>
          <nav class="menu mt-3 shadow p-3 mb-5 bg-white rounded">
            <ul class="list-unstyled mt-3" style="list-style-type: none;">
              <li class="nav-item">
                <a class="nav-link px-4" :href="`/wall/${userProfile.pk}`">Профиль</a>
              </li>
              <li class="nav-item">
                <a class="nav-link px-4" :href="`/profile/edit/${userProfile.pk}`">Редактирование профиля</a>
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
import axios from 'axios';

export default {
  data() {
    return {
      isAuthenticated: false,
      userProfile: null,
    };
  },
  created() {
    this.checkToken();
  },
  methods: {
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
        const id = localStorage.getItem('UserID')
        axios.get(`http://127.0.0.1:8000/api/profile/short/${id}/`, {
        headers: {
          Authorization: `token ${token}`,
        },
      })
      .then(response => {
        this.userProfile = response.data;
      })
      .catch(error => {
        console.error('Ошибка при получении данных пользователя:', error);
        this.logout();
      });
    },
    logout() {
      const token = localStorage.getItem('token');
      axios.post('http://127.0.0.1:8000/api/users/logout/', {}, {
        headers: {
          Authorization: `token ${token}`,
        },
      })
      .then(() => {
        localStorage.removeItem('token');
        this.isAuthenticated = false;
        this.userProfile = null;
        this.user = null;
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
  created() {
    this.checkToken();
  },
};
</script>

<style scoped>
@import '../../styles/profile/style-profile.css';
@import '../../styles/style-base.css';
@import '../../styles/profile/style-profile-v2.css';
</style>