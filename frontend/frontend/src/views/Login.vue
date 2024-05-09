<template>
    <div>
      <!-- HTML-разметка вашей страницы логина -->
      <div id="alerts"></div>
      <a href="#" class="navbar-brand logo-name-auth text-b-line"><b>НАЗВАНИЕ</b></a>
      <div class="container pos-auth">
        <h1 class="mb-4" style="font-size:40px; font-weight: bold;">Авторизация</h1>
        <p>У вас нет учетной записи? Тогда, пожалуйста <router-link to="Registration">зарегистрируйтесь</router-link></p>
        <form class="email" @submit.prevent="loginUser">
          <div class="mb-3">
            <input type="email" v-model="email" class="reg-all-input px-3" placeholder="Email address" autocomplete="email" maxlength="320" required>
          </div>
          <div class="mb-3">
            <input type="password" v-model="password" class="reg-all-input px-3" placeholder="Password" autocomplete="current-password" required>
            <br><br>
            <span class="helptext"><a href="#">Забыли пароль?</a></span>
          </div>
          <div class="mb-3">
            <label for="remember">Запомнить меня:</label>
            <input type="checkbox" v-model="remember" id="remember">
          </div>
          <div class="mb-3">
            <button type="submit" class="btn btn-primary mt-3">Login</button>
          </div>
        </form>
      </div>
      <div class="position-absolute top-0 end-0 d-none d-lg-block" style="width: 540px;">
        <img src="../assets/images/auth/login.jpg" alt="Изображение" class="img-fluid h-100">
      </div>
    </div>
  </template>
  
  <script>
  
  import { toast } from 'vue3-toastify';
  import 'vue3-toastify/dist/index.css';

  export default {
    data() {
      return {
        email: '',
        password: '',
        remember: false
      };
    },
    methods: {
      
      showErrorMessage(error){
          toast.error(error, {
            autoClose: 3000,
          });
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
              remember: this.remember
            })
          });

          const responseData = await response.json();
          
          if (responseData.key){
            const token = responseData.key; 
            localStorage.setItem('token', token);
            //сделать редирект на ленту
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
@import '../styles/style-auth.css'
</style>