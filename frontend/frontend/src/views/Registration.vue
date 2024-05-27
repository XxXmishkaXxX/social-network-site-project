<template>
  <div>
    <!-- Лого -->
    <a href="/" class="navbar-brand logo-name-auth text-b-line"><b>TellYou</b></a>

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

      <EmailConfirmation v-if="showCheckEmailButton" :email="email" @email-confirmed="handleEmailConfirmed" @error="showErrorMessage" />

    </div>

    <div class="position-absolute top-0 end-0 d-none d-lg-block" style="width: 540px;">
      <img src="../assets/images/auth/reg.jpg" alt="Изображение" class="img-fluid h-100">
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { API_BASE_URL } from '../config';
import EmailConfirmation from '../components/registration/CheckEmail.vue';
import { toastMixin } from '../mixins/toastMixin';

export default {
  components: {
    EmailConfirmation
  },
  data() {
    return {
      email: '',
      password1: '',
      password2: '',
      showCheckEmailButton: false
    };
  },
  mounted() {
    const storedButtonState = localStorage.getItem('showCheckEmailButton');
    if (storedButtonState) {
      this.showCheckEmailButton = JSON.parse(storedButtonState);
    }
  },
  mixins: [toastMixin],
  methods: {
    async registerUser() {
      try {
        const response = await axios.post(`${API_BASE_URL}/users/registration/`, {
          headers: {
            'Content-Type': 'application/json'
          },
          email: this.email,
          password1: this.password1,
          password2: this.password2
        });

        this.showCheckEmailButton = true;
        localStorage.setItem('showCheckEmailButton', JSON.stringify(true));
        this.showInfoMessage('На почту ' + this.email + ' пришло сообщение для подтверждения почты');

      } catch (error) {
        console.log(error);
        if (error.response.data.email)
          this.showErrorMessage(error.response.data.email);

        if (error.response.data.password1)
          this.showErrorMessage(error.response.data.password1);
        else
          this.showErrorMessage(error.response.data.non_field_errors);
      }
    },
    handleEmailConfirmed() {
      this.emailConfirmed = true;
      localStorage.removeItem('showCheckEmailButton');
      this.loginUser();
    },
    async loginUser() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/users/login/', {
          headers: {
            'Content-Type': 'application/json'
          },
          email: this.email,
          password: this.password1
        });

        const responseData = await response.data;
        if (responseData.key) {
          const token = responseData.key;
          const UserID = responseData.id;
          localStorage.setItem('token', token);
          localStorage.setItem('UserID', UserID);
          this.$router.push({ name: 'CreateProfile' });
        }
      } catch (error) {
        console.log(error);
        this.showErrorMessage(error);
      }
    }
  }
};
</script>

<style scoped>
@import '../styles/style-auth.css';
</style>
