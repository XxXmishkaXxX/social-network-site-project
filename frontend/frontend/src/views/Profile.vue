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
              <div class="full_name" style="max-width: 300px;">
                <h3>{{ userProfile.full_name }}</h3>
              </div>
              <div class="city" v-if="userProfile.city">
                <p>Город: {{ userProfile.city.name }}</p>
              </div>
              <br>
              <button @click="openModalProfileInfo" class="btn btn-outline-dark">Подробнее</button>

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
            </div>
            <div class="profile-container d-flex align-items-center" v-if="localStorage.getItem('UserID') === this.$route.params.UserID">
              <div class="main_info me-auto">
                <!-- main_info content here -->
              </div>
              <div class="edit_profile me-4">
                <router-link class="btn btn-primary" style="text-decoration: none; color:white;" :to="{ name: 'UpdateProfile', params: { userId: userProfile.id } }">
                  Редактировать профиль
                </router-link>
              </div>
              <UploadPostModal ref="uploadPostModal"/>
            </div>
          </div>
          <br>
          <div class="">
            <div class="container" id="postContainer">
              <div v-for="post in userProfile.posts" :key="post.id" class="card" :id="'post-' + post.id">
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

                <div v-if="post.video" class="video-container">
                  <video controls class="w-100">
                    <source :src="post.video.url" type="video/mp4">
                    Your browser does not support the video tag.
                  </video>
                </div>

                <div class="d-flex align-items-center">
                  <div class="like ms-3" id="like">
                    <button @click="likePost(post.id)" class="btn btn-outline-danger me-2 mt-4">
                      <b><i :id="'heart-svg-' + post.id" :class="{'bi bi-heart-fill': post.isLiked, 'bi bi-heart': !post.isLiked}"></i></b>
                      <b :id="'likes-count-' + post.id">{{ post.likes_count }}</b>
                    </button>
                  </div>

                  <div v-if="userProfile.user === localStorage.getItem('UserID')">
                    <form id="deleteForm">
                      <button type="button" class="me-2 btn btn-outline-dark" @click="deletePost(post.id)">Удалить</button>
                    </form>
                  </div>
                  <div class="views mt-4">
                    <i class="bi bi-eye"></i> <b>{{ post.views_count }} </b>
                  </div>
                </div>
                <br>

                <br>
                Комментарии
                 <div class="comments">
                  <h5>Комментарии</h5>
                  <div :id="'comments_list_' + post.id">
                    <div v-for="comment in post.comments" :key="comment.id" class="comment d-flex align-items-center">
                      <div class="avatar me-2">
                        <img :src="comment.user_profile.avatar" alt="avatar-commenter" style="max-width: 50px">
                      </div>
                      <div class="comment-info">
                        <div class="full_name">
                          <p>{{ comment.user_profile.full_name }}</p>
                        </div>
                        <div class="comment_text">{{ comment.text }}</div>
                        <div class="date-create-comment">{{ comment.created_at }}</div>
                      </div>
                    </div>
                  </div>
                  <form :id="'addComment_' + post.id" @submit.prevent="addComment(post.id)">
                    <div class="form-group">
                      <textarea :id="'commentText_' + post.id" class="form-control" rows="3" v-model="newComment"></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Отправить</button>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Футер -->
    <Footer />
  </div>
</template>

<script>
// Импорт компонентов навбара и футера
import Navbar from '../components/base/Navbar.vue';
import Footer from '../components/base/Footer.vue';
import axios from 'axios';
import UploadPostModal from '../components/Profile/UploadPostModal.vue';

export default {
  components: {
    Navbar,
    Footer,
    UploadPostModal
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
      newComment: ''
    };
  },
  created() {
    this.fetchUserProfile();
  },
  methods: {
    openUploadPostModal() {
      this.$refs.uploadPostModal.openModal();
    },
    openModalProfileInfo() {
      this.showModalProfileInfo = true;
    },
    closeModalProfileInfo() {
      this.showModalProfileInfo = false;
    },
    fetchUserProfile() {
      const UserID = this.$route.params.UserID;
      axios.get(`http://127.0.0.1:8000/api/profile/${UserID}/`)
        .then(response => {
          this.userProfile = response.data;
          console.log(this.userProfile)
        })
        .catch(error => {
          this.$router.push({ name: 'Home' });
        });
    },
    
    likePost(postId) {
      axios.post(`http://127.0.0.1:8000/api/posts/${postId}/like/`)
        .then(response => {
          this.fetchUserPosts();
        })
        .catch(error => {
          console.error(error);
        });
    },
    deletePost(postId) {
      axios.delete(`http://127.0.0.1:8000/api/posts/${postId}/`)
        .then(response => {
          this.fetchUserPosts();
        })
        .catch(error => {
          console.error(error);
        });
    },
    addComment(postId) {
      axios.post(`http://127.0.0.1:8000/api/posts/${postId}/comments/`, {
        text: this.newComment
      })
        .then(response => {
          this.newComment = '';
          this.fetchUserPosts();
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
};
</script>

<style scoped>
@import '../styles/modal-windows/profile-info.css';
@import '../styles/profile/style-profile.css';
@import '../styles/profile/style-profile-v2.css';
</style>
