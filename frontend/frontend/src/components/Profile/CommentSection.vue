<template>
    <div class="comments">
      <h5>Комментарии</h5>
      <div :id="'comments_list_' + post.id">
        <div v-for="comment in post.comment_for_post" :key="comment.id" class="comment d-flex align-items-center">
          <div class="avatar me-2">
            <img :src="comment.user_profile_avatar" alt="avatar-commenter" class="rounded-circle me-3" width="50" height="50">
          </div>
          <div class="comment-info">
            <div class="commenter-name">
              <a :href="'/wall/' + comment.user_profile">
                <p>{{ comment.user_profile_name }}</p>
              </a>
            </div>
            <div class="comment_text">{{ comment.text }}</div>
            <div class="date-create-comment">{{ comment.created_at }}</div>
          </div>
        </div>
      </div>
      <form :id="'addComment_' + post.id" @submit.prevent="addComment(post.id)">
        <div class="form-group">
          <textarea :id="'commentText_' + post.id" class="form-control" rows="1" v-model="newComment"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Отправить</button>
      </form>
    </div>
  </template>
  
  <script>
import axios from 'axios';
import { API_BASE_URL } from '../../config';

  export default {
    props: ['post'],
    data() {
      return {
        newComment: ''
      };
    },
    methods: {
      async addComment(postId) {
        const token = localStorage.getItem('token');
        const response = await axios.post(`${API_BASE_URL}/wall/comment/create/`, {
            post_id: postId,
            text: this.newComment
        }, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `token ${token}`
            }
        })
          .then(response => {
            this.newComment = '';
            this.$emit('comment-added');
          })
          .catch(error => {
            console.error(error);
          });
      }
    }
  };
  </script>
  
  <style scoped>
  @import '../../styles/profile/comments.css'
  

  </style>
  