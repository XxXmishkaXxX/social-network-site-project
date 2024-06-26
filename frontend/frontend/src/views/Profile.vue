<template>
  <div>
    <Navbar />
    <div class="main-container d-flex flex-row">
      <SideBar />
      <div class="profile">
        <div class="profile-container d-flex align-items-center">
          <div class="main d-flex align-items-center">
            <div class="avatar">
              <img :src="userProfile.avatar" alt="avatar" class="ava-pre-img">
            </div>
            <div class="profile-info ms-4 me-2" style="margin-top: 20px;">
              <div class="full_name">
                <h3>{{ userProfile.full_name }}</h3>
              </div>
              <div class="city" v-if="userProfile.city">
                <p>Город: {{ userProfile.city.name }}</p>
              </div>
              <!-- Кнопка для открытия модального окна -->
              <button class="btn btn-info" style="margin-top: 20px; color:white;" @click="openModalUserInfo">Подробнее</button>
              
              <div class="modal fade" id="userInfoModal" tabindex="-1" aria-labelledby="userInfoModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title" id="userInfoModalLabel">Информация о пользователе</h5>
                    </div>
                    <div class="modal-body">
                      <p>Страна: {{ userProfile.country ? userProfile.country.name : 'Не указан' }}</p>
                      <p>Город: {{ userProfile.city ? userProfile.city.name : 'Не указан' }}</p>
                      <p>Дата рождения: {{ userProfile.birth_date}}</p>
                      <p>Пол: {{ userProfile.sex}}</p>
                      <p>О себе: {{ userProfile.bio}}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-if="userProfile.user == localStorage.getItem('UserID')" class="d-flex align-items-center">
            <router-link class="btn btn-primary me-4" style="text-decoration: none; color: white;" :to="{ name: 'UpdateProfile', params: { userId: userProfile.id } }">
              Редактировать профиль
            </router-link>
            <UploadPostModal />
          </div>
          <div v-if="userProfile.user != localStorage.getItem('UserID')" class="d-flex align-items-center">
            <ButtonAddFriend
              v-if="userProfile.user && userProfile.is_friend !== undefined"
              :userProfileId="userProfile.user"
              :isFriend="userProfile.is_friend.is_friend"
              :isRequestSentToUser="userProfile.is_friend.is_request_sent_to_user"
              :isRequestSentFromUser="userProfile.is_friend.is_request_sent_from_user"
              @update:isFriend="handleUpdateIsFriend"
              @update:isRequestSentToUser="handleUpdateIsRequestSentToUser"
              @update:isRequestSentFromUser="handleUpdateIsRequestSentFromUser"
            />
            <ButtonFollow  v-if="userProfile.user && userProfile.is_following !== undefined"
              :userProfileId="userProfile.user" 
              :isFollowing="userProfile.is_following" 
              @update:isFollowing="handelUpdateFollowStatus" />
          </div>
        </div>
        <br>
        <div class="postContainer"><br>
          <div v-for="post in posts" :key="post.id" class="card mb-4" :id="'post-' + post.id">
            <div class="card-body">
              <p class="date">{{ post.created_at }}</p>
              <p class="card-text">{{ post.content }}</p>
              <div class="container_images">
                <div v-for="image in post.images" :key="image.id" class="col">
                  <div class="thumbnail">
                    <div class="img-container">
                      <img :src="image.image" alt="Post Image" class="img-fluid" style="border-radius: 15px;" @click="openModalImg(image.image)">
                    </div>
                  </div>
                </div>
              </div>
              <div class="d-flex align-items-center mt-3">
                <LikeButton :postId="post.id" :liked="post.liked" :likesCount="post.likes_count" @update="fetchPostById(post.id)" />
                <DeletePostButton v-if="userProfile.user == localStorage.getItem('UserID')" :isUserPost="true" :post-id="post.id" @post-deleted="fetchUsersPosts" />
              </div>
              <hr>
              <CommentSection :post="post" @comment-added="fetchPostById(post.id)" />
            </div>
          </div>
          <!-- Modal -->
          <div class="modal fade" id="imageModal" tabindex="-1" aria-labelledby="imageModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-xl"> 
              <div class="modal-content">
                  <img :src="currentImage" alt="Modal Image"> 
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
import DeletePostButton from '../components/Profile/DeletePostButton.vue';
import LikeButton from '../components/Profile/LikeButton.vue';
import ButtonAddFriend from '../components/Profile/ButtonAddFriend.vue';
import { API_BASE_URL } from '../config';
import SideBar from '../components/base/SideBar.vue';
import { Modal } from 'bootstrap';
import ButtonFollow from '../components/Profile/ButtonFollow.vue';

export default {
  components: {
    Navbar,
    Footer, 
    UploadPostModal,
    CommentSection,
    DeletePostButton,
    LikeButton,
    ButtonAddFriend,
    SideBar,
    ButtonFollow
  },
  data() {
    return {
      localStorage: window.localStorage,
      userProfile: {
        country: { id: '', name: '' },
        city: {},
        avatar: '',
        sex: '',
        birth_date: '',
        bio: '',
        is_friend: '',
        is_following: ''
      },
      posts: [],
      currentImage: null,
    };
  },
  mounted() {
    this.fetchUserProfile();
  },
  methods: {

    handleUpdateIsFriend(newValue) {
      this.userProfile.is_friend.is_friend = newValue;
    },
    handleUpdateIsRequestSentToUser(newValue) {
      this.userProfile.is_friend.is_request_sent_to_user = newValue;
    },

    handleUpdateIsRequestSentFromUser(newValue){
      this.userProfile.is_friend.is_request_sent_from_user = newValue;
      this.userProfile.is_friend.is_friend = true
    },
    
    handelUpdateFollowStatus(newValue) {
      this.userProfile.is_following = newValue
    },
    openModalImg(image) {
      this.currentImage = image;
      const modal = new Modal(document.getElementById('imageModal'));
      modal.show();
    },
    closeModalImg() {
      const modal = new Modal(document.getElementById('imageModal'));
      modal.hide();
    },
    openModalUserInfo() {
      const modal = new Modal(document.getElementById('userInfoModal'))
      modal.show()
    },
    closeModalUserInfo() {
      const modal = new Modal(document.getElementById('userInfoModal'))
      modal.hide()  
    },
    fetchUserProfile() {
      const UserID = this.$route.params.UserID;

      axios.get(`${API_BASE_URL}/profile/wall/${UserID}/`, {
        headers: {
          'Authorization': `token ${localStorage.getItem('token')}`
        }
      })
        .then(response => {
          this.userProfile = response.data;
          this.fetchUsersPosts();
        })
        .catch(error => {
          console.error('Error fetching user profile:', error);
          this.$router.push({ name: 'Home' });
        });
    },
    fetchUsersPosts() {
      const UserID = this.$route.params.UserID;
      axios.get(`${API_BASE_URL}/wall/posts/${UserID}/`, {
        headers: {
          'Authorization': `token ${localStorage.getItem('token')}`
        }
      })
      .then(response => {
        this.posts = response.data.posts;
      })
      .catch(error => {
        console.error('Error fetching user posts:', error);
      });
    },
    async fetchPostById(postId){
      const response = await axios.get(`${API_BASE_URL}/wall/post/${postId}/`, {
          headers: {
            Authorization: `token ${localStorage.getItem('token')}`
          }
        });
        const post = response.data
        const postIndex = this.posts.findIndex(post => post.id === postId);
        if (postIndex !== -1) {
          this.posts[postIndex] = post
        }
    },
  }
};
</script>

<style scoped>
@import '../styles/profile/header-profile.css';
@import '../styles/profile/content-profile.css';

.main-container {
  margin: 10px 10px 200px 200px;
  width: 80%;
  flex-direction: column;
  align-items: flex-start;
}

.profile {
  margin-right: 350px;
  margin-left: 10px;
  width: 1100px;
}
</style>
