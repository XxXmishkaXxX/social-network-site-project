<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-navbar">
    <div class="container-fluid">
      <a href="/" class="navbar-brand logo-name text-b-line"><b>TellYou</b></a>
      <button type="button" class="navbar-toggler logo-button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <div class="navbar-nav ms-auto logo-button">
          <MenuHomePage />
        </div>
      </div>
    </div>
  </nav>
</template>

  <script>

  import MenuHomePage from './MenuHomePage.vue';

  export default {
    components: {
      MenuHomePage // Регистрация компонента Menu
    }
  };
  </script>
  
  <style scoped>
  @import url("../../styles/style-base.css");

  </style>
  