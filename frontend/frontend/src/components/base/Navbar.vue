<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-navbar">
    <div class="container-fluid d-flex justify-content-between align-items-center">
      <a href="/" class="navbar-brand logo-name text-b-line"><b>TellYou</b></a>
      <button type="button" class="navbar-toggler logo-button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
        <span class="navbar-toggler-icon"></span>
      </button>
      <Notifications v-if="userToken"/>
      <MenuHomePage />
    </div>
  </nav>
</template>

  <script>

  import MenuHomePage from './MenuHomePage.vue';

  export default {
    components: {
      MenuHomePage, 
    },

    data() {
      return {
        userToken: localStorage.getItem('token')
      };
    },

  };
  </script>
  
  <style scoped>
  @import url("../../styles/style-base.css");

  </style>
  