<template>
  <div class="container mt-5">
    <form method="post" enctype="multipart/form-data" @submit.prevent="submitForm">
      <div v-if="step === 1">
        <h2 class="h2-create mt-2">Создание профиля</h2>
        <h5><i class="mt-3">Для начала нам нужно познакомиться. Как к вам можно обращаться?</i></h5>
        <br>
        <div>
          <label for="firstName" class="mb-3">Имя:</label>
          <input type="text" id="firstName" class="form-control create-all-input px-3" v-model="userData.firstName">
          
          <label for="lastName" class="mb-3">Фамилия:</label>
          <input type="text" id="lastName" v-model="userData.lastName" class="form-control create-all-input px-3">
        </div>
        <div class="d-none d-md-block col-md-6 align-self-center img-create">
            <img src="../assets/images/createProfile/sol.png" alt="Изображение" class="img-fluid">
        </div>
      <div class="button-container">
        <button type="button" class="btn btn-primary" @click="nextStep">Далее</button>
      </div>
      </div>

      <div v-else-if="step === 2">
        <h2 class="h2-create mt-2">Создание профиля</h2>
        <h5 style="width: 50rem;"><i class="mt-3">Отлично! Приятно познакомиться.
          А теперь, если не возражаете, не могли бы загрузить Ваше фото и ввести неуоторые данные.</i></h5>

        <div class="mb-3">
          <label for="avatar" class="form-label">Аватар:</label>
          <br>
          <img id="avatarPreview" :src="avatarPreviewUrl" alt="Предварительный просмотр аватара"
          style="width: 128px; height: 128px;" class="avatar-preview img-thumbnail avatar-pre-img">
          <span>128px</span>
          
          <img id="avatarPreview2" :src="avatarPreviewUrl" alt="Avatar Preview"
                     class="avatar-preview img-thumbnail avatar-pre-img2" style="width: 96px; height: 96px;">
          <span>96px</span>

          <img id="avatarPreview3" :src="avatarPreviewUrl" alt="Avatar Preview"
                     class="avatar-preview img-thumbnail avatar-pre-img3" style="width: 64px; height: 64px;">
          <span>64px</span>
          
          <input id="avatar" type="file" name="avatar" @change="previewAvatar" class="form-control mt-5 i-size2 w-25">
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
          <VueDatePicker 
            id="birth_date" 
            name="birth_date"
            class="w-25"
            v-model="userData2.date" 
            :format="format"
            :min-date="minBirthDate"
            :max-date="maxBirthDate">
        </VueDatePicker>
          
        </div>

        <div class="d-none d-md-block col-md-6 align-self-center img-create">
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

        <div class="d-none d-md-block col-md-6 align-self-center img-create">
                <img src="../assets/images/createProfile/kot.png" alt="Изображение" class="img-fluid">
        </div>
        <br>
        <div class="button-container">
          <button type="button" class="btn btn-primary" @click="prevStep">Назад</button>
          <button class="btn btn-success" type="submit">Создать</button>
        </div>
      </div>
      
    </form>
  </div>
</template>

<script>

  import VueDatePicker from '@vuepic/vue-datepicker';
  import '@vuepic/vue-datepicker/dist/main.css'
  import axios from 'axios';
  import { toast } from 'vue3-toastify';
  import 'vue3-toastify/dist/index.css';

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
        avatar: null,
        sex: 'M',
        date: null
      },
      userData3:{
        bio: '',
        country: null,
        city: null
      },
      avatarPreviewUrl: '../src/assets/images/createProfile/default_avatar.jpg',
      minBirthDate: minBirthDate,
      maxBirthDate: maxBirthDate
    };
  },
  methods: {
    format(date) {
      const day = date.getDate();
      const month = date.getMonth() + 1;
      const year = date.getFullYear();

      return `${year}-${month}-${day}`;
    },
    showErrorMessage(error){
          toast.error(error, {
            autoClose: 3000,
          });
      },
    nextStep() {
      if (this.step === 1 && (!this.userData.firstName || !this.userData.lastName)) {
        this.showErrorMessage('Пожалуйста, введите имя и фамилию.');
        return;
      }
      else if (this.step === 2 && (!this.userData2.date)) {
        this.showErrorMessage('Пожалуйста, выберете дату рождения');
        return;
      }

      this.step++;
    },
    prevStep() {
      this.step--;
    },
    previewAvatar(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.avatarPreviewUrl = e.target.result;
        };
        reader.readAsDataURL(file);
        this.userData2.avatar = file
      }
    },
    async fetchCountries() {
      if (!this.countriesLoaded) { // Проверяем, был ли уже выполнен запрос
        try {
            const response = await axios.get('http://127.0.0.1:8000/api/profile/get_countries/');
            this.countries = response.data;
            this.countriesLoaded = true; // Устанавливаем флаг загрузки стран
        } catch (error) {
            console.error('Ошибка при получении списка стран:', error);
        }
    }
    },
    async fetchCities(countryId) {
        try {
            const response = await axios.get('http://127.0.0.1:8000/api/profile/get_cities_by_country/'+countryId+'/');
            this.cities = response.data; // предположим, что сервер возвращает массив объектов городов
        } catch (error) {
            console.error('Ошибка при получении списка городов:', error);
        }
    },
    async onCountryChange() {
        if (this.userData3.country) {
            await this.fetchCities(this.userData3.country);
            document.getElementById('city_div').style.display = 'block'; // отображаем блок выбора города
        } else {
            this.userData3.city = null; // сбрасываем выбранный город, если страна не выбрана
            document.getElementById('city_div').style.display = 'none'; // скрываем блок выбора города
        }
    },
    async submitForm() {
      console.log(this.userData2.avatar)
      try {
          const formData = new FormData();
          formData.append('full_name', this.userData.firstName + '|' + this.userData.lastName);
          formData.append('avatar', this.userData2.avatar);
          formData.append('sex', this.userData2.sex);
          formData.append('birth_date', `${this.userData2.date.getFullYear()}-${this.userData2.date.getMonth()+1}-${this.userData2.date.getDate()}`);
          formData.append('bio', this.userData3.bio);
          formData.append('country', this.userData3.country);
          formData.append('city', this.userData3.city);

          const response = await fetch('http://127.0.0.1:8000/api/profile/create/', {
            method: 'POST',
            headers: {
              'Authorization': 'token '+localStorage.getItem('token')
            },
            body: formData,
            })
          const responseData = await response.json();
          
          console.log(responseData)
          if (responseData.status) {
            this.$router.push('/');
          }
          if (responseData.birth_date){
            this.showErrorMessage('Введенная вами дата не соответствует правилам')
          }
          if(responseData.full_name){
            this.showErrorMessage(responseData.full_name)
          }

        } catch (error) {
            this.showErrorMessage(error);
        }
    },
  }
};


</script>

<style scoped>
@import '../styles/createProfile/style-profile-v2.css';
@import '../styles/createProfile/style-profile.css';
.button-container {
        display: flex;
        gap: 10px;
        margin-top: 20px;
    }
</style>
