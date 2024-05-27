<template>
        <div>
          <form v-if="!codeConfirmed" @submit.prevent="submitCode">
            <div class="form-group">
              <label for="code">Введите код:</label>
              <input type="text" class="form-control" id="code" v-model="code">
            </div>
            <button type="submit" class="btn btn-primary">Отправить</button>
          </form>
          <ResetPasswordComplete v-if="codeConfirmed" :uid="this.uid" :code="this.code" />
        </div>
  </template>
  
  <script>
  import ResetPasswordComplete from '../resetPassword/ResetPasswordComplete.vue'
  import  {toastMixin}  from '../../mixins/toastMixin';
  import axios from 'axios';
  export default {
    data() {
      return {
        code: '',
        codeConfirmed: false,
        uid: ''
      };
    },
    mixins: [toastMixin],
    components: {ResetPasswordComplete},
    methods: {
        async submitCode() {
                try {
                    const response = await axios.post('http://127.0.0.1:8000/api/users/password/reset/confirm/', {
                        code: this.code
                    });
                    this.uid = response.data.uid
                    this.codeConfirmed = true
                } catch (error) {
                    const responseDataError = error.response.data.detail
                    this.showErrorMessage(responseDataError);
                }
            }
    }
  };
  </script>
  
  <style scoped>
  .container {
    margin-top: 50px;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  </style>
  