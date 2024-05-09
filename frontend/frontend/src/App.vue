<script setup>
import { RouterView } from 'vue-router';
import Navbar from './components/base/Navbar.vue';
import Footer from './components/base/Footer.vue';
</script>

<template>
  <div id="root">
    <section class="section">
      <RouterView />
    </section>  
  </div>
</template>


<style scoped>

</style>