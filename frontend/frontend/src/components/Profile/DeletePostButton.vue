<template>
    <div v-if="isUserPost">
      <form id="deleteForm">
        <button type="button" class="me-2 btn btn-outline-dark" @click="deletePost">Удалить</button>
      </form>
    </div>
  </template>
  
  <script>
  import { API_BASE_URL } from '../../config';

  export default {
    props: {
      isUserPost: Boolean,
      postId: Number
    },
    methods: {
      deletePost() {
        fetch(`${ API_BASE_URL }/wall/posts/${this.postId}/`, {
          method: 'DELETE',
          headers: {
            'Authorization': `token ${localStorage.getItem('token')}`
          }
        })
          .then(response => {
            this.$emit('post-deleted');
          });
      }
    }
  };
  </script>
  
  <style scoped>
  /* Добавьте ваши стили для кнопки удаления поста */
  </style>
  