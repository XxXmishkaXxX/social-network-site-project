<template>
  <div>
    <div class="container mt-5">
      <form method="post" enctype="multipart/form-data" @submit.prevent="submitForm">
        <div v-if="step === 1">
          <h2 class="h2-create mt-2">Создание профиля</h2>
          <h5><i class="mt-3">Для начала нам нужно познакомиться. Как к вам можно обращаться?</i></h5>
          <br>
          <div>
            <label for="firstName" class="mb-3">Имя:</label>
            <input type="text" id="firstName" class="form-control create-all-input px-3" v-model="userData.firstName">
            <br>
            <label for="lastName" class="mb-3">Фамилия:</label>
            <input type="text" id="lastName" v-model="userData.lastName" class="form-control create-all-input px-3">
          </div>
          <div class="d-none d-md-block align-self-center img-create">
            <img src="../assets/images/createProfile/sol.png" alt="Изображение" class="img-fluid">
          </div>
          <div class="button-container">
            <button type="button" class="btn btn-primary" @click="nextStep">Далее</button>
          </div>
        </div>

        <div v-else-if="step === 2">
          <h2 class="h2-create mt-2">Создание профиля</h2>
          <h5 style="width: 50rem;"><i class="mt-3">Отлично! Приятно познакомиться. А теперь, если не возражаете, не могли бы загрузить Ваше фото и ввести некоторые данные.</i></h5>

          <div class="mb-3">
            <label for="avatar" class="form-label">Аватар:</label>
            <br>
            <img id="avatarPreview" :src="avatarPreviewUrl" alt="Предварительный просмотр аватара"
              style="width: 128px; height: 128px;" class="avatar-preview img-thumbnail avatar-pre-img me-1">
            <span class="me-2">128px</span>
            
            <img id="avatarPreview2" :src="avatarPreviewUrl" alt="Avatar Preview"
              class="avatar-preview img-thumbnail avatar-pre-img2 me-1" style="width: 96px; height: 96px;">
            <span class="me-2">96px</span>

            <img id="avatarPreview3" :src="avatarPreviewUrl" alt="Avatar Preview"
              class="avatar-preview img-thumbnail avatar-pre-img3 me-1" style="width: 64px; height: 64px;">
            <span class="me-2">64px</span>
            <input id="avatar" type="file" @change="onFileChange" class="form-control mt-5 w-25">
          </div>

          <div class="mb-3">
            <label for="sex" class="form-label mb-3">Пол:</label>
            <select id="sex" name="sex" class="form-select create-all-input px-3 w-25" v-model="userData2.sex">
              <option value="M">Мужчина</option>
              <option value="F">Женщина</option>
            </select>
          </div>

          <div class="mb-3">
            <label for="birth_date" class="form-label">Дата рождения:</label>
            <VueDatePicker id="birth_date" name="birth_date" class="w-25" v-model="userData2.date" :format="format" :min-date="minBirthDate" :max-date="maxBirthDate"></VueDatePicker>
          </div>

          <div class="d-none d-md-block align-self-center img-create">
            <img src="../assets/images/createProfile/za.png" alt="Изображение" class="img-fluid">
          </div>

          <div class="button-container">
            <button type="button" class="btn btn-primary" @click="prevStep">Назад</button>
            <button type="button" class="btn btn-primary" @click="nextStep">Далее</button>
          </div>
        </div>

        <div v-else-if="step === 3">
          <h2 class="h2-create mt-2">Создание профиля</h2>
          <h5 style="width: 50rem;"><i class="mt-3">Хорошо, а теперь не могли бы рассказать что-то о себе?</i></h5>

          <br>

          <div class="mb-3">
            <label for="bio" class="form-label">О себе</label>
            <textarea id="bio" name="bio" rows="3" class="form-control bio-adap-create" v-model="userData3.bio"></textarea>
          </div>

          <div class="mb-3">
            <label for="country" class="form-label mb-3">Страна</label>
            <select id="country" name="country" class="form-select create-all-input px-3" v-model="userData3.country" @click="fetchCountries" @change="onCountryChange">
              <option v-for="country in countries" :key="country.id" :value="country.id">{{ country.name }}</option>
            </select>
          </div>

          <div id="city_div" v-if="userData3.country" class="mb-3">
            <label for="city" class="form-label mb-3">Город</label>
            <select id="city" name="city" class="form-select create-all-input px-3" v-model="userData3.city">
              <option value="0">Выбрать город</option>
              <option v-for="city in cities" :key="city.id" :value="city.id">{{ city.name }}</option>
            </select>
          </div>

          <div class="d-none d-md-block align-self-center img-create">
            <img src="../assets/images/createProfile/kot.png" alt="Изображение" class="img-fluid">
          </div>
          <br>
          <div class="button-container">
            <button type="button" class="btn btn-primary" @click="prevStep">Назад</button>
            <button class="btn btn-success" type="submit">Создать</button>
          </div>
        </div>
      </form>

      <!-- Модальное окно для обрезки изображения -->
      <div class="modal" id="cropperModal" tabindex="-1" aria-labelledby="cropperModalLabel" aria-hidden="true"  data-bs-backdrop="static">
        <div class="modal-dialog modal-lg modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="cropperModalLabel">Обрезка изображения</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="cancelCrop"></button>
            </div>
            <div class="modal-body">
              <div class="cropper-box">
                <img id="imgToCrop" :src="cropImageUrl" class="img-fluid">
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="cancelCrop">Отмена</button>
              <button type="button" class="btn btn-primary" @click="cropImage">Обрезать и сохранить</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';
import axios from 'axios';
import { toastMixin } from '../mixins/toastMixin';
import 'vue3-toastify/dist/index.css';
import { API_BASE_URL } from '../config';
import Cropper from 'cropperjs';
import 'cropperjs/dist/cropper.css';
import { Modal } from 'bootstrap'


export default {
  components: {
    VueDatePicker
  },
  data() {
    const today = new Date();
    const maxBirthDate = new Date(today.getFullYear() - 14, today.getMonth(), today.getDate());
    const minBirthDate = new Date(today.getFullYear() - 120, today.getMonth(), today.getDate());

    return {
      countries: [],
      countriesLoaded: false,
      cities: [],
      step: 1,
      userData: {
        firstName: '',
        lastName: ''
      },
      userData2: {
        avatar: '',
        sex: 'M',
        date: null
      },
      userData3: {
        bio: '',
        country: '',
        city: ''
      },
      avatarPreviewUrl: '../src/assets/images/createProfile/default_avatar.jpg',
      cropImageUrl: '',
      imageReady: false,
      minBirthDate: minBirthDate,
      maxBirthDate: maxBirthDate,
      cropper: null
    };
  },
  mixins: [toastMixin],
  methods: {
    format(date) {
      const day = date.getDate();
      const month = date.getMonth() + 1;
      const year = date.getFullYear();
      return `${year}-${month}-${day}`;
    },

    nextStep() {
      if (this.step === 1 && (!this.userData.firstName || !this.userData.lastName)) {
        this.showErrorMessage('Пожалуйста, введите имя и фамилию.');
        return;}
      
      else if (this.userData.firstName.length < 2 || this.userData.lastName.length < 2) {
        this.showErrorMessage('Имя или фамилия должны быть длиннее одного символа');
          return;
      } else if (/[^a-zA-Zа-яА-ЯёЁ]/.test(this.userData.firstName) || /[^a-zA-Zа-яА-ЯёЁ]/.test(this.userData.lastName)) {
          this.showErrorMessage('Имя и фамилия не должны содержать спецсимволы и цифры');
          return;
      } else if (this.step === 2 && (!this.userData2.date)) {
        this.showErrorMessage('Пожалуйста, выберете дату рождения');
        return;
      }
      this.step++;
    },
    prevStep() {
      this.step--;
    },
    onFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.cropImageUrl  = e.target.result;
          const cropperModal = new Modal(document.getElementById('cropperModal'));
          cropperModal.show();
          this.$nextTick(() => {
            const imageElement = document.getElementById('imgToCrop');
            this.cropper = new Cropper(imageElement, {
              aspectRatio: 1,
              viewMode: 1,
            });
          });
        };
        reader.readAsDataURL(file);
      }
    },
    cropImage() {
      const canvas = this.cropper.getCroppedCanvas();
      this.avatarPreviewUrl = canvas.toDataURL();
      canvas.toBlob((blob) => {
        const file = new File([blob], 'avatar.jpg', { type: 'image/jpeg' });
        this.userData2.avatar = file;
      });
      this.cropper.destroy();
      const cropperModal = Modal.getInstance(document.getElementById('cropperModal'));
      cropperModal.hide();
    },
    cancelCrop() {
      this.cropImageUrl = '';
      document.getElementById('avatar').value = '';
      if (this.cropper) {
        this.cropper.destroy();
        this.cropper = null;
      }
    },
    async fetchCountries() {
      if (!this.countriesLoaded) {
        try {
          const response = await axios.get(`${API_BASE_URL}/profile/get_countries/`);
          this.countries = response.data;
          this.countriesLoaded = true;
        } catch (error) {
          console.error('Error fetching countries:', error);
        }
      }
    },
    async fetchCities(countryId) {
      try {
        const response = await axios.get(`${API_BASE_URL}/profile/get_cities_by_country/${countryId}/`);
        this.cities = response.data;
      } catch (error) {
        console.error('Error fetching cities:', error);
      }
    },
    async onCountryChange() {
      if (this.userData3.country) {
        await this.fetchCities(this.userData3.country);
        document.getElementById('city_div').style.display = 'block';
      } else {
        this.userData3.city = null;
        document.getElementById('city_div').style.display = 'none';
      }
    },
    async submitForm() {
      const formData = new FormData();
      console.log(this.userData2.avatar)
      formData.append('full_name', `${this.userData.firstName}|${this.userData.lastName}`);
      formData.append('avatar', this.userData2.avatar);
      formData.append('sex', this.userData2.sex);
      formData.append('birth_date', `${this.userData2.date.getFullYear()}-${this.userData2.date.getMonth() + 1}-${this.userData2.date.getDate()}`);
      formData.append('bio', this.userData3.bio);
      formData.append('country', this.userData3.country);
      formData.append('city', this.userData3.city);

      try {
        const response = await axios.post(`${API_BASE_URL}/profile/create/`, formData, {
          headers: {
            'Authorization': 'token ' + localStorage.getItem('token'),
            'Content-Type': 'multipart/form-data'
          }
        });
        this.$router.push('/wall/' + localStorage.getItem('UserID') + '/');
      } catch (error) {
        this.showErrorMessage('Error creating profile.');
      }
    }
  }
};
</script>

<style scoped>

@import '../styles/profile/create-profile.css';

</style>
