<template>
  <div>
    <!-- Навбар -->
    <Navbar />

    <!-- Содержимое профиля -->
    <div class="container">
      <div class="row">
        <div class="col-12" style="background-color: #FBF8F8; padding: 2rem; margin: 0 auto;">
          <br><br><br><br>
          <div class="profile-container d-flex align-items-center" style="border-radius:25px;">
            <div class="avatar">
              <img :src="userProfile.avatar" alt="avatar" class="ava-pre-img">
            </div>
            <div class="profile-info ms-7" style="max-width: 300px;">
              <div class="full_name">
                <h3>{{ userProfile.full_name }}</h3>
              </div>
              <div class="city" v-if="userProfile.city">
                <p>Город: {{ userProfile.city.name }}</p>
              </div>
              <button @click="openModalProfileInfo" class="btn btn-outline-dark">Подробнее</button>
            </div>
            <div class="edit_profile me-4">
              <router-link class="btn btn-primary" style="text-decoration: none; color:white;" :to="{ name: 'UpdateProfile', params: { userId: userProfile.id } }">
                Редактировать профиль
              </router-link>
            </div>
            <div class="upload_post">
              <UploadPostModal />
            </div>
          </div>

          <div v-if="showModalProfileInfo" class="modal">
            <div class="modal-content">
              <div class="info">
                <span @click="closeModalProfileInfo" class="close">&times;</span>
                <div class="birth_date">
                  <p>{{ userProfile.birth_date }}</p>
                </div>
                <div class="country">
                  <p>{{ userProfile.country.name }}</p>
                </div>
                <div class="city">
                  <p>{{ userProfile.city.name }}</p>
                </div>
                <div class="bio">
                  <p>{{ userProfile.bio }}</p>
                </div>
              </div>
            </div>
          </div>
          <br>
          <div class="">
            <div class="postContainer" id="postContainer">
              <div v-for="post in posts" :key="post.id" class="card" :id="'post-' + post.id">
                <p class="date"><br>&nbsp;&nbsp;&nbsp;&nbsp;Дата публикации: {{ post.created_at }}</p>
                <p class="card-text"><br>&nbsp;&nbsp;&nbsp;&nbsp;{{ post.content }}</p>
                <div class="container_images">
                  <div class="row">
                    <div v-if="post.images && post.images.length" class="row row-cols-2">
                      <div v-for="image in post.images" :key="image.id" class="col-lg-6">
                        <div class="thumbnail">
                          <div class="img-container ms-3">
                            <img :src="image.image" alt="Post Image" style="max-width: 1000px; border-radius: 20px;">
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="d-flex align-items-center">

                  <LikeButton :postId="post.id" :liked="post.liked" :likesCount="post.likes_count" @update="fetchUsersPosts" />

                  <DeletePostButton v-if="userProfile.user == localStorage.getItem('UserID')" :isUserPost="true" 
                  :post-id="post.id" @post-deleted="fetchUsersPosts" />
                </div>
                <br>

                <br>
                <CommentSection :post="post" @comment-added="fetchUsersPosts" />
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

import Navbar from '../components/base/Navbar.vue';
import Footer from '../components/base/Footer.vue';
import axios from 'axios';
import UploadPostModal from '../components/Profile/UploadPostModal.vue';
import CommentSection from '../components/Profile/CommentSection.vue';
import DeletePostButton from '../components/Profile/DeletePostButton.vue'
import LikeButton from '../components/Profile/LikeButton.vue';
import { API_BASE_URL } from '../config';

export default {
  components: {
    Navbar,
    Footer,
    UploadPostModal,
    CommentSection,
    DeletePostButton,
    LikeButton
  },
  data() {
    return {
      localStorage: window.localStorage,
      showModalProfileInfo: false,
      userProfile: {
        country: { id: '', name: '' },
        city: {},
        avatar: '',
        sex: '',
        birth_date: '',
        bio: ''
      },
      posts: [],
    };
  },
  created() {
    this.fetchUserProfile();
  },
  methods: {
    
    fetchUserProfile() {
      const UserID = this.$route.params.UserID;
      axios.get(`${API_BASE_URL}/profile/wall/${UserID}/`)
        .then(response => {
        
          this.userProfile = response.data;
          this.fetchUsersPosts()
        })
        .catch(error => {
          this.$router.push({ name: 'Home' });
        });
    },

    fetchUsersPosts(){
      const UserID = this.$route.params.UserID;
      axios.get(`${API_BASE_URL}/wall/posts/${UserID}/`, {
        headers: {
          'Authorization': `token ${localStorage.getItem('token')}`
        }}
      )
      .then(response => {

        this.posts = response.data.posts
      })

    },
  }
};
</script>


<style scoped>
 @import '../styles/profile/header-profile.css';
 @import '../styles/profile/content-profile.css';
</style>