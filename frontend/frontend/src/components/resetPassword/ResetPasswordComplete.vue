<template>

     <form @submit.prevent="submitPassword">
            <div class="form-group">
              <label for="password">Новый пароль:</label>
              <input type="password" class="form-control" id="password" v-model="password" placeholder="Введите новый пароль">
            </div>
            <br>
            <div class="form-group">
              <label for="confirmPassword">Подтвердите новый пароль:</label>
              <input type="password" class="form-control" id="confirmPassword" v-model="confirmPassword" placeholder="Подтвердите новый пароль">
            </div>
            <br>
            <button type="submit" class="btn btn-primary">Сохранить</button>
     </form>

  </template>

<script>
import  {toastMixin}  from '../../mixins/toastMixin';
  import axios from 'axios';
export default {
  data() {
    return {
      password: '',
      confirmPassword: ''
    };
  },
  mixins:[toastMixin],
  props: {
    uid: {},
    code: {},
  },
  methods: {
    async submitPassword() {
        try {   
                    const response = await axios.post('http://127.0.0.1:8000/api/users/password/reset/complete/', {
                        uid: this.uid,
                        code: this.code,
                        new_password: this.password,
                        confirm_password: this.confirmPassword

                    });
                    window.location.href = '/login'; 

                } catch (error) {
                    this.showErrorMessage(error.response.data.non_field_errors);

                }

    }
  }
};
</script>