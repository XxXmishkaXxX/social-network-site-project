<template>
    <div>
      <!-- Лого -->
      <a href="#" class="navbar-brand logo-name-auth text-b-line" ><b>НАЗВАНИЕ</b></a>
  
      <!-- Форма -->
      <div class="container pos-auth">
        <h1 class="mb-4" style="font-size:40px; font-weight: bold;">Регистрация</h1>
  
        <p>У вас уже есть аккаунт? Тогда, пожалуйста <router-link :to="{ name: 'Login' }">войдите</router-link>.</p>
        <br>
        <form class="signup" @submit.prevent="registerUser">
          <div class="mb-3">
            <input type="email" v-model="email" class="reg-all-input px-3" placeholder="example@mail.ru" autocomplete="email" maxlength="320" required>
          </div>
          <div class="mb-3">
            <input type="password" v-model="password1" class="reg-all-input px-3" placeholder="Пароль" autocomplete="new-password" required>
          </div>
          <div class="mb-3">
            <input type="password" v-model="password2" class="reg-all-input px-3" placeholder="Повторение пароля" autocomplete="new-password" required>
          </div>
          <button class="btn btn-primary mt-4" type="submit">Регистрация</button>
        </form>

        <button v-if="showCheckEmailButton" :class="{ 'btn-success': emailConfirmed }" class="btn mt-2" @click="checkEmail">{{ emailConfirmed ? 'Подтверждено' : 'Проверить почту' }}</button>

      </div>
      
      <div class="position-absolute top-0 end-0 d-none d-lg-block" style="width: 540px;">
        <img src="../assets/images/auth/reg.jpg" alt="Изображение" class="img-fluid h-100">
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
        password1: '',
        password2: '',
        showCheckEmailButton: false,
        emailConfirmed: false

      };
    },
    mounted() {

    const storedButtonState = localStorage.getItem('showCheckEmailButton');
    if (storedButtonState) {
      this.showCheckEmailButton = JSON.parse(storedButtonState);
      }
    },
    methods: {
      showErrorMessage(error){
          toast.error(error, {
            autoClose: 3000,
          });
      },

      showSuccessMessage(message){
        toast.info(message, {
          autoClose: 3000,
        });
      },

      async registerUser() {
        try {
          const response = await fetch('http://127.0.0.1:8000/api/users/registration/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              email: this.email,
              password1: this.password1,
              password2: this.password2
            })
          });

          const responseData = await response.json();
          if (responseData.detail === 'Verification e-mail sent.') {
            this.showCheckEmailButton = true;
            localStorage.setItem('showCheckEmailButton', JSON.stringify(true));
            this.showSuccessMessage('На почту '+ this.email + ' пришло сообщение для подтверждения почты')
          }
          else if (responseData.email){
            this.showErrorMessage(responseData.email)
          }
          else{
            this.showErrorMessage(responseData.non_field_errors)
          }

        } catch (error) {
            console.log(error)
            this.showErrorMessage(error);
        }
      },
      async checkEmail() {
        try {
          const response = await fetch('http://127.0.0.1:8000/api/users/check-email-verify/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              email: this.email
            })
          });
          const responseData = await response.json();

          if (responseData.status) {
              this.emailConfirmed = true;
              localStorage.removeItem('showCheckEmailButton');
              const loginResponse = this.loginUser(this.email, this.password1);
              
            }
          else{

            this.showErrorMessage('Почта не подтверждена!')
          }

        } catch (error) {
            this.showErrorMessage(error)
        }
      },

      async loginUser(){
        try{
        const response = await fetch('http://127.0.0.1:8000/api/users/login/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              email: this.email,
              password: this.password1
            })
          });

          const responseData = await response.json();
          if (responseData.key){
            
            const token = responseData.key; 
            const UserID = responseData.id;
            localStorage.setItem('token', token);
            localStorage.setItem('UserID', id)
            this.$router.push({name: 'CreateProfile'});
          }
        } 
          catch(error){
            this.showErrorMessage(error)
          }
    }
    }
};
  </script>


  <style scoped>
  @import '../styles/style-auth.css';
  .btn-success {
  background-color: #28a745;
  color: #fff;}
  </style>