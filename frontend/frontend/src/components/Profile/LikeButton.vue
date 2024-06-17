<template>
    <div class="like ms-3" id="like">
      <button @click="likePost" class="btn btn-outline-danger me-2">
        <b>
          <i :id="'heart-svg-' + postId" :class="heartClass"></i>
        </b>
        <b :id="'likes-count-' + postId">{{ likesCount }}</b>
      </button>
    </div>
  </template>
  
  <script>
  import { API_BASE_URL } from '../../config';

  export default {
    props: {
      postId: null,
      liked: null,
      likesCount: null
    },
    computed: {
      heartClass() {
        return {
          'bi bi-heart-fill': this.liked.includes(this.userId),
          'bi bi-heart': !this.liked.includes(this.userId)
        };
      },
      userId() {
        return parseInt(localStorage.getItem('UserID'));
      }
    },
    methods: {
      likePost() {
        const response = fetch(`${ API_BASE_URL }/wall/posts/like/${this.postId}/`, {
          method: 'GET',
          headers: {
            'Authorization': `token ${localStorage.getItem('token')}`
          }
        }).then(response => {
          this.$emit('update');
        });
      }
    }
  };
  </script>
  