<template>
  <div>
    <Navbar />
    <div class="container mt-5">
      <h2>Редактирование профиля</h2>
      <div class="row ms-custom-edit">
        <div class="col-md-3">
          <div class="d-grid gap-2 mt-5" style="max-width: 200px;">
            <button @click="showSection('basic_info')" class="btn btn-outline-primary">Основное</button>
            <button @click="showSection('avatar')" class="btn btn-outline-primary">Аватар</button>
            <button @click="showSection('about_me')" class="btn btn-outline-primary">О себе</button>
            <button @click="showSection('change_password')" class="btn btn-outline-primary">Изменить пароль</button>
            <a class="mt-2 abtn" :href="'/'">На главную</a>
          </div>
        </div>
        <div class="col-md-8"><br><br>
          <div class="svdig-forms">
            <form @submit.prevent="submitForm" enctype="multipart/form-data">
              <div v-if="userProfile">
                <div v-if="currentSection === 'basic_info'">
                  <div class="mb-3">
                    <label for="last_name" class="form-label">Фамилия:</label>
                    <input class="form-control edit-all-input mt-2" id="last_name" type="text" v-model="lastName">
                  </div>
                  <div class="mb-3">
                    <label for="first_name" class="form-label">Имя:</label>
                    <input id="first_name" class="form-control edit-all-input mt-2" type="text" v-model="firstName">
                  </div>
                  <div class="mb-3">
                    <label for="birth_date" class="form-label">Дата рождения:</label>
                    <VueDatePicker 
                      id="birth_date" 
                      name="birth_date"
                      class="w-25"
                      v-model="userProfile.birth_date" 
                      :format="format"
                      :min-date="minBirthDate"
                      :max-date="maxBirthDate">
                    </VueDatePicker>
                    
                  </div>
                  <div class="mb-3">
                    <label for="sex" class="form-label">Пол:</label>
                    <select id="sex" name="sex" v-model="userProfile.sex" class="form-select edit-all-input">
                      <option value="F">Женщина</option>
                      <option value="M">Мужчина</option>
                      
                    </select>
                  </div>
                  <div class="mb-3">
                    <label for="country" class="form-label">Страна:</label>
                    <select class="form-select edit-all-input" id="country" name="country" v-model="userProfile.country.id" @change="onCountryChange">
                      <option v-for="country in countries" :key="country.id" :value="country.id">{{ country.name }}</option>
                    </select>
                  </div>
                  <div id="city_div" v-if="userProfile.country" class="mb-3">
                    <label for="city" class="form-label">Город:</label>
                    <select id="city" name="city" class="form-select edit-all-input" v-model="userProfile.city.id">
                      <option v-for="city in cities" :key="city.id" :value="city.id">{{ city.name }}</option>
                    </select>
                  </div>
                  <div class="d-none d-md-block col-md-6 align-self-center img-avatar-osnova">
                    
                  </div>
                </div>
                <div v-else-if="currentSection === 'about_me'">
                  <div class="mb-1 mx-auto">
                    <label for="bio" class="form-label">Биография:</label>
                    <textarea id="bio" v-model="userProfile.bio" rows="3" class="form-control bio-adap"></textarea>
                  </div>
                  <div class="d-none d-md-block col-md-6 align-self-center img-avatar-osnova">
                    
                  </div>
                  <br><br><br><br><br><br><br><br><br><br><br><br><br>
                </div>  
                <div v-else-if="currentSection === 'avatar'">
                  <div class="row">
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
                  </div>
                  <br><br><br><br><br><br><br>
                </div>
                <ChangePassword :currentSection="currentSection" />
              </div>
              <button v-if="currentSection !== 'change_password'" type="submit" class="btn btn-success">Сохранить</button>
              <span>&nbsp;</span>
              <button v-if="currentSection !== 'change_password'" class="btn btn-danger">Отмена</button>
            </form>
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
      </div>
    </div>
    <Footer />
  </div>
</template>
  
  <script>
  import Footer from '@/components/base/Footer.vue';
  import Navbar from '@/components/base/Navbar.vue';
  import VueDatePicker from '@vuepic/vue-datepicker';
  import '@vuepic/vue-datepicker/dist/main.css'
  import axios from 'axios';
  import ChangePassword from '@/components/Profile/ChangePassword.vue';
  import  {toastMixin}  from '../mixins/toastMixin';
  import Cropper from 'cropperjs';
  import 'cropperjs/dist/cropper.css';
  import { Modal } from 'bootstrap'

  export default {
  components: {
    Navbar,
    Footer,
    VueDatePicker,
    ChangePassword
  },
  data() {
    const today = new Date();
    const maxBirthDate = new Date(today.getFullYear() - 14, today.getMonth(), today.getDate());
    const minBirthDate = new Date(today.getFullYear() - 120, today.getMonth(), today.getDate());
    return {
      userProfile: {
        country: {id:'',name:''},
        city: {id:'',name:''},
        avatar: '',
        sex: '',
        birth_date: '',
        bio: '',
        last_name: '',
        first_name: ''
      },
      currentSection: 'basic_info',
      lastName: '',
      firstName: '',
      countries: [],
      cities: [],
      countriesLoaded: false,
      avatarChanged: false,
      minBirthDate: minBirthDate,
      maxBirthDate: maxBirthDate,
      cropper: null,
      avatarPreviewUrl: null,
      cropImageUrl: null,
    };
  },
  mounted() {
    this.fetchUserData();
  },
  computed: {
    fullName() {
      return `${this.firstName}|${this.lastName}`;
    }
  },
  mixins: [toastMixin],
  methods: {
    format(date) {
      const day = date.getDate();
      const month = date.getMonth() + 1;
      const year = date.getFullYear();
      return `${year}-${month}-${day}`;
    },
    showSection(section) {
      this.currentSection = section;
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
        this.userProfile.avatar = file;
      });
      this.cropper.destroy();
      const cropperModal = Modal.getInstance(document.getElementById('cropperModal'));
      cropperModal.hide();
      this.avatarChanged = true
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
          const response = await axios.get('http://127.0.0.1:8000/api/profile/get_countries/');
          this.countries = response.data;
          this.countriesLoaded = true;
        } catch (error) {
          console.error('Ошибка при получении списка стран:', error);
        }
      }
    },
    async fetchCities(countryID) {
      try {
        this.cities = [];
        console.log(countryID);
        const response = await axios.get(`http://127.0.0.1:8000/api/profile/get_cities_by_country/${countryID}/`);
        this.cities = response.data;
      } catch (error) {
        console.error('Ошибка при получении списка городов:', error);
      }
    },
    async onCountryChange() {
      if (this.userProfile.country) {
        await this.fetchCities(this.userProfile.country.id);
      } else {
        this.userProfile.city = null;
      }
    },
    fetchUserData() {
      axios.get(`http://127.0.0.1:8000/api/profile/edit/`, {
        headers: { Authorization: 'token ' + localStorage.getItem('token') }
      })
      .then(response => {
        this.avatarPreviewUrl = response.data.avatar
        if (response.data.country === null) { response.data.country = { id: '', name: '' } }
        if (response.data.city === null) { response.data.city = { id: '', name: '' } }
        this.userProfile = response.data;

        const fullNameParts = this.userProfile.full_name.split(' ');
        
        this.firstName = fullNameParts[0];
        this.lastName = fullNameParts.slice(1).join(' ');
        
        return this.fetchCountries();
      })
      .then(() => {
        if (this.userProfile.country) {
          return this.fetchCities(this.userProfile.country.id);
        }
      })
      .catch(error => {
        console.error('Ошибка при получении данных пользователя:', error);
        this.$router.push({ name: 'Home' });
      });
    },
    async submitForm() {
      try {
        const formData = new FormData();
        formData.append('full_name', this.fullName);
        if (this.avatarChanged) {
          formData.append('avatar', this.userProfile.avatar);
        }
        formData.append('sex', this.userProfile.sex);
        formData.append('birth_date', this.userProfile.birth_date);
        formData.append('bio', this.userProfile.bio);
        formData.append('country', this.userProfile.country.id);
        formData.append('city', this.userProfile.city.id);

        const config = {
            headers: {
              'Authorization': 'Token ' + localStorage.getItem('token'), 
              'Content-Type': 'multipart/form-data' 
              }
            };

        const response = await axios.put(`http://127.0.0.1:8000/api/profile/edit/`, formData, config);
        
        this.showSuccessMessage("Данные сохранены")
      
      } catch (error) {

        const errorMessage = error.response.data.full_name[0]
        console.log(errorMessage)
        this.showErrorMessage(errorMessage)
      }
    }
  }
};
</script>


  <style scoped>
@import '../styles/profile/update-profile.css';
@import url('../styles/style-base.css');
</style>