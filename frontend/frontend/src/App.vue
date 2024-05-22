<script setup>
import { RouterView } from 'vue-router';

</script>

<template>
  <div id="root">
    <section class="section">
      <RouterView />
    </section>  
  </div>
</template>


<style scoped>
  @import url('./styles/style-base.css');
  @import url('./styles/bootstrap/bootstrap.css')
</style>