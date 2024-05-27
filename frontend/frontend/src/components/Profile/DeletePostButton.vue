<template>
    <div v-if="isUserPost">
      <form id="deleteForm">
        <button type="button" class="me-2 btn btn-outline-dark" @click="deletePost">Удалить</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      isUserPost: Boolean,
      postId: Number
    },
    methods: {
      deletePost() {
        fetch(`http://127.0.0.1:8000/api/wall/posts/${this.postId}/`, {
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
  