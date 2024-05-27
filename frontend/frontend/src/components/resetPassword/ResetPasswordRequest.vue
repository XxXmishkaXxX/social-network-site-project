<template>
    <div>
        <div class="d-flex align-items-center justify-content-center vh-100">
            <div class="col-md-4">
                <div class="card">
                <div class="card-body">
                    <h2 class="card-title text-center">Сброс пароля</h2>
                    <div v-if="!sendedMail">
                        <form @submit.prevent="requestReset">
                            <div class="mb-3">
                                <label for="email" class="form-label">Email:</label>
                                <input type="email" id="email" v-model="email" class="form-control" required />
                            </div>
                            <button type="submit" class="btn btn-primary w-100">Сбросить пароль</button>
                        </form>
                    </div>
                    <div v-if="sendedMail">
                        <ResetPasswordConfirmVue />
                    </div>
                </div>
            </div>
        </div>
        </div>
    </div>
  </template>
  
  <script>
    import  {toastMixin}  from '../../mixins/toastMixin';
    import axios from 'axios';

    import ResetPasswordConfirmVue from './ResetPasswordConfirm.vue';
  
    export default {
    
        mixins: [toastMixin],
        
        data() {
            return {
                email: '',
                sendedMail: false
                };
            },
        
        components:{ResetPasswordConfirmVue},
        methods: {

            async requestReset() {
                try {
                    await axios.post('http://127.0.0.1:8000/api/users/password/reset/request/', {
                        email: this.email
                    });
                    this.showInfoMessage('Проверьте свою электронную почту на наличие кода для сброса.');
                    this.sendedMail = true
                } catch (error) {
                    this.showErrorMessage('Ошибка при запросе на сброс пароля:', error);
                }
            }
        }
    };
  </script>

<style scoped>
.vh-100 {
  height: 100vh;
}
</style>