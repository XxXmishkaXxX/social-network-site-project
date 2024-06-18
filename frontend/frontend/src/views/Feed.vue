<template>
  
  <div class="d-flex flex-column min-vh-100">
    <Navbar />
    <div class="main-container d-flex flex-row flex-grow-1">
      <SideBar />
      <div class="content-container">
        <div class="header-buttons d-flex justify-content-between align-items-center mb-3">
          <button class="btn btn-outline-primary" @click="fetchAllPosts">Все</button>
          <div class="ml-auto">
            <button class="btn btn-outline-primary me-2" @click="fetchFriendsPosts">Друзья</button>
            <button class="btn btn-outline-primary" @click="fetchSubscriptionPosts">Подписки</button>
          </div>
        </div>
        <div class="modal fade" id="imageModal" tabindex="-1" aria-labelledby="imageModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-xl"> 
              <div class="modal-content">
                  <img :src="currentImage" alt="Modal Image"> 
              </div>
            </div>
          </div>

          <div class="postContainer">
              <div v-for="post in posts" :key="post.id" class="card mb-4" :id="'post-' + post.id">
                <div class="card-body" style="border-radius: 20px;">
                  <div class="d-flex align-items-center me-3 head-post">
                    <img :src="post.author_profile.avatar" alt="Avatar" class="rounded-circle me-3" width="50" height="50">
                    <a :href="'/wall/' + post.author_profile.pk">
                      <span>{{ post.author_profile.full_name }}</span>
                    </a>
                  </div>
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
                    <LikeButton :postId="post.id" 
                                :liked="post.liked" 
                                :likesCount="post.likes_count"
                                @update="fetchPostById(post.id)" 
                    />
                  </div>
                  <hr>
                  <CommentSection :post="post" @comment-added="fetchPostById(post.id)"/>
                </div>
              </div>
          <InfiniteLoading @infinite="fetchPosts" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import InfiniteLoading from 'v3-infinite-loading';
import { API_BASE_URL } from '../config';
import Navbar from '@/components/base/Navbar.vue';
import SideBar from '@/components/base/SideBar.vue';
import LikeButton from '../components/Profile/LikeButton.vue';
import CommentSection from '../components/Profile/CommentSection.vue';
import { Modal } from 'bootstrap';



export default {
  name: 'PostsContainer',
  components: {
    InfiniteLoading,
    Navbar,
    SideBar,
    LikeButton,
    CommentSection
  },
  data() {
    return {
      posts: [],
      currentPage: 1,
      perPage: 10,
      loading: false,
      url: '/posts/all/',
      currentImage: null,
    };
  },
  methods: {
    async fetchPosts($state) {
      try {
        const response = await axios.get(`${API_BASE_URL}/feed${this.url}`, {
          headers: {
            Authorization: `token ${localStorage.getItem('token')}`
          },
          params: {
            page: this.currentPage,
            per_page: this.perPage
          }
        });
        const newPosts = response.data.results;
        console.log(newPosts)

        if (newPosts.length > 0) {
          this.posts = [...this.posts, ...newPosts];
          this.currentPage++;
          $state.loaded();
        } 
        $state.loaded();
        
      } catch (error) {
        
      }

    },
    fetchAllPosts() {
      this.posts = [];
      this.currentPage = 1;
      this.url = '/posts/all/';
    },
    fetchFriendsPosts() {
      this.posts = [];
      this.currentPage = 1;
      this.url = '/posts/friends-posts/';
    },
    fetchSubscriptionPosts() {
      this.posts = [];
      this.currentPage = 1;
      this.url = '/posts/subscriptions-posts/';
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
    }
  }
};
</script>


<style scoped>

.post {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ccc;
}

.content-container {
    background-color: #fff;
    border-radius: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
    width: 800px;
    padding-bottom: 20px;
    margin-left: 20px;
    min-height: 500px; 
    max-height: 100%
}
.main-container {
    margin: 10px 10px 400px 300px;
    width: 80%;
    flex-direction: column;
    align-items: flex-start;
}
.posts-container {
  overflow-y: auto;
}

.post {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #ffffff;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.post h3 {
  margin-bottom: 10px;
  font-size: 1.5rem;
  color: #343a40;
}

.post p {
  margin: 0;
  font-size: 1rem;
  color: #6c757d;
}
.head-post p{
  margin: 0;
  font-weight: bold;
}

.head-post a{
  color: inherit;
  text-decoration:none;
}
</style>
