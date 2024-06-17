<template>
    <div v-if="currentSection === 'change_password'">
        <form @submit.prevent="changePasswordForm">
            <div class="mb-3">
                <label for="id_oldpassword" class="form-label">Текущий пароль:</label>
                <input type="password" class="form-control edit-all-input" v-model="oldPassword" name="oldpassword"
                    placeholder="Текущий пароль" autocomplete="current-password" required id="id_oldpassword">
            </div>
            <div class="mb-3">
                <label for="id_password1" class="form-label">Новый пароль:</label>
                <input type="password" class="form-control edit-all-input" v-model="newPassword1" name="password1"
                    placeholder="Новый пароль" autocomplete="new-password" required aria-describedby="id_password1_helptext" id="id_password1">
                <span class="helptext" id="id_password1_helptext"></span>
            </div>
            <ul>
                <li style="width: 50%;">Ваш пароль не должен быть слишком похож на другие ваши персональные данные.</li>
                <li>Ваш пароль должен содержать не менее 8 символов.</li>
                <li>Ваш пароль не может быть обычным паролем.</li>
                <li>Ваш пароль не может быть полностью цифровым.</li>
            </ul>
            <div class="mb-3">
                <label for="id_password2" class="form-label">Новый пароль(повторить):</label>
                <input type="password" class="form-control edit-all-input" v-model="newPassword2" name="password2"
                    placeholder="Новый пароль(повторить)" required id="id_password2">
            </div>
            <button name="change_password_button" type="submit" class="btn btn-success">Изменить текущий пароль</button>
        </form>
    </div>
</template>

<script>
    import { toast } from 'vue3-toastify';
  import 'vue3-toastify/dist/index.css';
  import { API_BASE_URL } from '../../config';

export default {
    props: ['currentSection'],
    data() {
        return {
            oldPassword: '',
            newPassword1: '',
            newPassword2: ''
        };
    },
    methods: {

        showErrorMessage(error){
          toast.error(error, {
            autoClose: 3000,
          });
      },

      showSuccessMessage(message){
        toast.success(message, {
          autoClose: 3000,
        });
      },

        async changePasswordForm() {
            try {
                const formData = new FormData();
                formData.append('old_password', this.oldPassword);
                formData.append('new_password1', this.newPassword1);
                formData.append('new_password2', this.newPassword2);

                const response = await fetch(`${ API_BASE_URL }/users/change-password/`, {
                    method: 'POST',
                    headers: {
                        'Authorization': 'token ' + localStorage.getItem('token')
                    },
                    body: formData,
                });

                const responseData = await response.json();
                if (response.ok) {
                    this.showSuccessMessage('Пароль успешно изменен');
                } else {
                    if (responseData.old_password)
                        this.showErrorMessage('Старый пароль неверный');
                    else{
                        this.showErrorMessage(responseData.new_password1)
                    }
                }
            } catch (error) {
                console.error(error);
            }
        }
    }
};
</script>
