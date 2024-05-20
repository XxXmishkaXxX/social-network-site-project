<template>
    <div>
      <!-- Навбар -->
      <Navbar />
    
      <!-- Содержимое профиля -->
      <div class="container">
        <div class="row">
          <div class="col-12" style="background-color: #FBF8F8; padding: 2rem; margin: 0 auto; ">
            <br><br><br><br>
            <div class="profile-container d-flex align-items-center " style="border-radius:25px;">
              <div class="avatar">
                <img :src="userProfile.avatar" alt="avatar" class="ava-pre-img">
              </div>
              <div class="profile-info ms-7 " style="max-width: 300px;">
                <div class="full_name" style="max-width: 300px;">
                  <h3>{{ userProfile.full_name }}</h3>
                </div>
                <div class="city" v-if="userProfile.city">
                  <p>Город: {{ userProfile.city.name }}</p>
                </div>
                <br>
                <button id="openModalBtn" class="btn btn-outline-dark">Подробнее</button>
  
                <div id="modal" class="modal">
                  <div class="modal-content">
                    <div class="info">
                      <span class="close">&times;</span>
                      <div class="birth_date">
                        <p>{{ userProfile.birth_date }}</p>
                      </div>
                      <div class="country">
                        <p>{{ userProfile.country.name }}</p>
                      </div>
                      <div class="city">
                        <p>{{ userProfile.city.name }}</p>
                      </div>
                      <div class="bio">
                        <p>{{ userProfile.bio }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="profile-container d-flex align-items-center" v-if="localStorage.getItem('UserID') === this.$route.params.UserID">
                <div class="main_info me-auto">
                  <!-- main_info content here -->
                </div>
                <div class="edit_profile me-4">
                  <router-link class="btn btn-primary" style="text-decoration: none; color:white;" :to="{ name: 'UpdateProfile', params: { userId: userProfile.id } }">
                    Редактировать профиль
                  </router-link>
                </div>
                <div class="add_post">
                  <button id="openModalFormCreatePostBtn" class="btn btn-success">Загрузить работу</button>
                </div>
              </div>
            </div>
            <br>
          </div>
        </div>
      </div>
      <!-- Футер -->
      <Footer />
    </div>
  </template>
  
  <script>
  // Импорт компонентов навбара и футера
  import Navbar from '../components/base/Navbar.vue';
  import Footer from '../components/base/Footer.vue';
  import axios from 'axios';
  import router from '@/router';

  export default {

    components: {
      Navbar,
      Footer,
    },
    data() {
      return {
        localStorage: window.localStorage,
        showModalProfileInfo: false,
        userProfile: {
            country: {id:'',name:''},
            city: {},
            avatar: '',
            sex: '',
            birth_date: '',
            bio: '',}
      };
    },
    created() {
      
      this.fetchUserProfile();
    },
    methods: {
        openModalProfileInfo() {
            console.log("!")
            this.showModalProfileInfo = true;
        },
        closeModalProfileInfo() {
            this.showModalProfileInfo = false;
        },

        fetchUserProfile() {
        // Получение данных профиля из API, используя UserID из параметров маршрута
            const UserID = this.$route.params.UserID;
            // Выполнение запроса к API для получения профиля
            // Замените эту часть кода соответствующим кодом для вашего API
            // Например:
            axios.get(`http://127.0.0.1:8000/api/profile/${UserID}/`)
                .then(response => {
                    this.userProfile = response.data;
                    console.log(this.userProfile)
                })
                .catch(error => {
                    this.$router.push({ name: 'Home'});
                });
        }
    }
  };
  </script>
  
  <style scoped>
  @import '../styles/modal-windows/profile-info.css';
  @import '../styles/createProfile/style-profile.css';
@import '../styles/createProfile/style-profile-v2.css';
  </style>
  