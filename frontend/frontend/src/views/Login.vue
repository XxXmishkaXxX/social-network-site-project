<template>
    <div>
      <!-- HTML-разметка вашей страницы логина -->
      <a href="/" class="navbar-brand logo-name-auth text-b-line"><b>TellYou</b></a>
      <div v-if="!isResetPassword" class="container pos-auth">
        <h1 class="mb-4" style="font-size:40px; font-weight: bold;">Авторизация</h1>
        <p>У вас нет учетной записи? Тогда, пожалуйста <router-link to="Registration">зарегистрируйтесь</router-link></p>
        <form class="email" @submit.prevent="loginUser">
          <div class="mb-3">
            <input type="email" v-model="email" class="reg-all-input px-3" placeholder="Email address" autocomplete="email" maxlength="320" required>
          </div>
          <div class="mb-3">
            <input type="password" v-model="password" class="reg-all-input px-3" placeholder="Password" autocomplete="current-password" required>
            <br><br>
            <button type="button" class="btn btn-link p-0" @click="showResetPassword">Забыли пароль?</button>
          </div>
          <div class="mb-3">
            <button type="submit" class="btn btn-primary mt-3">Login</button>
          </div>
        </form>
      </div>
      <div v-if="isResetPassword">
        <ResetPasswordRequestVue />
      </div>
      <div class="position-absolute top-0 end-0 d-none d-lg-block" style="width: 540px;">
        <img src="../assets/images/auth/login.jpg" alt="Изображение" class="img-fluid h-100">
      </div>
    </div>
  </template>
  
  <script>
  
  import { toast } from 'vue3-toastify';
  import 'vue3-toastify/dist/index.css';
  import router from '@/router';
  import axios from 'axios';
  import { toastMixin } from '@/mixins/toastMixin';

  import ResetPasswordRequestVue from '../components/resetPassword/ResetPasswordRequest.vue';
  
  export default {
    mixins: [toastMixin],
    data() {
      return {
        email: '',
        password: '',
        isResetPassword: false
      };
    },
    components:{
      ResetPasswordRequestVue
    },
    methods: {
      
      showResetPassword() {
        this.isResetPassword = true;
      },

      async loginUser() {
        try {
          const response = await fetch('http://127.0.0.1:8000/api/users/login/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              email: this.email,
              password: this.password,
            })
          });

          const responseData = await response.json();
          
          if (responseData.key){
            const token = responseData.key;
            const UserID = responseData.id;
            console.log(responseData)
            localStorage.setItem('token', token);
            localStorage.setItem('UserID', UserID)

            try {
              const response = await axios.get(`http://127.0.0.1:8000/api/profile/wall/${UserID}/`, {
              headers: {
                  Authorization: `token ${token}`
              }
              });
              router.push({ name: 'Profile', params: { UserID: UserID }});
          } catch (error) {

            if (error.response.status === 404) {
                    this.$router.push({ name: 'CreateProfile' });
                } 
          } 
          }
          else{
            this.showErrorMessage(responseData.non_field_errors)
          }

        } catch (error) {
          this.showErrorMessage(error);
        }
      }
    }
  };
  </script>
  

  <style scoped>
  @import '../styles/style-auth.css';
  </style>