<template>
  <div>
    <!-- Navbar -->
    <Navbar />

    <!-- Содержимое профиля -->
    <div class="container-fluid">
      <div class="row">
        <SidePanel />
        <div class="col-md-9 ml-sm-auto col-lg-8 px-4" style="background-color: #FBF8F8; padding: 2rem; margin: 0 auto; border-radius: 25px;">
          <div class="profile-container d-flex justify-content-between align-items-center">
            <div class="main d-flex align-items-center">
              <div class="avatar">
                <img :src="userProfile.avatar" alt="avatar" class="ava-pre-img">
              </div>
              <div class="profile-info ms-4" style="max-width: 300px;">
                <div class="full_name">
                  <h3>{{ userProfile.full_name }}</h3>
                </div>
                <div class="city" v-if="userProfile.city">
                  <p>Город: {{ userProfile.city.name }}</p>
                </div>
              </div>
            </div>
            <div v-if="userProfile.user == localStorage.getItem('UserID')" class="d-flex align-items-center">
              <router-link class="btn btn-primary me-4" style="text-decoration: none; color: white;" :to="{ name: 'UpdateProfile', params: { userId: userProfile.id } }">
                Редактировать профиль
              </router-link>
              <UploadPostModal />
            </div>
            <div v-else>
              <ButtonAddFriend />
            </div>
          </div>
          <br>
          <div class="postContainer">
            <div v-for="post in posts" :key="post.id" class="card mb-4" :id="'post-' + post.id">
              <div class="card-body">
                <p class="date">Дата публикации: {{ post.created_at }}</p>
                <p class="card-text">{{ post.content }}</p>
                <div class="container_images">
                  <div class="row row-cols-2">
                    <div v-for="image in post.images" :key="image.id" class="col">
                      <div class="thumbnail">
                        <div class="img-container">
                          <img :src="image.image" alt="Post Image" class="img-fluid" style="border-radius: 20px;">
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="d-flex align-items-center mt-3">
                  <LikeButton :postId="post.id" :liked="post.liked" :likesCount="post.likes_count" @update="fetchUsersPosts" />
                  <DeletePostButton v-if="userProfile.user == localStorage.getItem('UserID')" :isUserPost="true" :post-id="post.id" @post-deleted="fetchUsersPosts" />
                </div>
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
import ButtonAddFriend from '../components/Profile/ButtonAddFriend.vue'
import { API_BASE_URL } from '../config';
import SidePanel from '../components/base/SidePanel.vue';


export default {
  components: {
    Navbar,
    Footer, 
    UploadPostModal,
    CommentSection,
    DeletePostButton,
    LikeButton,
    ButtonAddFriend,
    SidePanel
  },
  data(){
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
  mounted() {
    this.fetchUserProfile();
  },
  methods: {
    
    fetchUserProfile() {
      const UserID = this.$route.params.UserID;
      axios.get(`${API_BASE_URL}/profile/wall/${UserID}/`)
        .then(response => {
        
          this.userProfile = response.data;
          console.log(this.userProfile)
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
