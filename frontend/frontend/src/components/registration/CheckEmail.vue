<template>
    <div>
      <button :class="{ 'btn-success': emailConfirmed }" class="btn btn-light mt-2" @click="checkEmail">
        {{ emailConfirmed ? 'Подтверждено' : 'Проверить почту' }}
      </button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { API_BASE_URL } from '../../config';
  
  export default {
    props: ['email'],
    data() {
      return {
        emailConfirmed: false
      };
    },
    methods: {
      async checkEmail() {
        try {
          const response = await axios.post(`${API_BASE_URL}/users/check-email-verify/`, {
            headers: {
              'Content-Type': 'application/json'
            },
            email: this.email
          });
  
          this.emailConfirmed = true;
          this.$emit('email-confirmed');
  
        } catch (error) {
          this.$emit('error', error.response.data.status);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .btn-success {
    background-color: #28a745;
    color: #fff;
  }
  </style>
  