<template>
  <div class="comments">
    <h5>Комментарии {{ post.comment_for_post.length }}</h5>
    <div :id="'comments_list_' + post.id">
      <div v-for="comment in displayedComments" :key="comment.id" class="comment d-flex align-items-center">
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
    <button v-if="!showAllComments && shouldShowMoreButton" @click="showMore" class="btn btn-link">Показать все комментарии</button>
    <button v-if="showAllComments" @click="showLess" class="btn btn-link">Скрыть комментарии</button>
    
    <!-- Форма отправки комментария всегда видна -->
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
import  {toastMixin}  from '../../mixins/toastMixin';

export default {
  props: ['post'],
  data() {
    return {
      newComment: '',
      maxVisible: 3, // Initial number of visible comments
      showAllComments: false // Flag to show all comments
    };
  },
  computed: {
    displayedComments() {
      if (this.showAllComments) {
        return this.post.comment_for_post;
      } else {
        return this.post.comment_for_post.slice(0, this.maxVisible);
      }
    },
    shouldShowMoreButton() {
      return !this.showAllComments && this.maxVisible < this.post.comment_for_post.length;
    }
  },

  mixins: [toastMixin],

  methods: {
    async addComment(postId) {

      if (this.newComment.trim() === '') {
        this.showErrorMessage('Комментарий не может быть пустым!');
        return;
      }

      const token = localStorage.getItem('token');
      try {
        await axios.post(`${API_BASE_URL}/wall/comment/create/`, {
          post_id: postId,
          text: this.newComment
        }, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `token ${token}`
          }
        });
        this.newComment = '';
        this.$emit('comment-added');
      } catch (error) {
        console.error(error);
      }
    },
    showMore() {
      this.showAllComments = true;
    },
    showLess() {
      this.showAllComments = false;
    }
  }
};
</script>

<style scoped>
@import '../../styles/profile/comments.css';
</style>
