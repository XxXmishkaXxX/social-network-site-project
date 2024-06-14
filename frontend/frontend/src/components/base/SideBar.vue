<template>
  <div class="sidebar">
    <ul class="nav flex-column">
      <li class="nav-item">
        <a class="nav-link" :href="'/wall/'+userID">Моя страница</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :href="'/feed/'">Лента</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :href="'/friends/'">Друзья</a>
      </li>
    </ul>
  </div>
</template>

<script>
 export default {
    data() {
        return {
            userID: null,
        }
    },
    mounted() {
        this.userID = localStorage.getItem('UserID');
    }
  }
</script>

<style scoped>
.sidebar {
  width: 200px;
  height: 270px;
  background-color: #f8f9fa;
  padding: 15px;
  border-right: 1px solid #ddd;
  border-radius: 25px;
  background-color: #ffffff;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  margin-left: 100px;
}

.nav {
  list-style: none;
  padding: 0;
}

.nav-item {
  margin-bottom: 10px;
}

.nav-link {
  display: block;
  padding: 10px;
  color: #343a40;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s, color 0.3s;
}

.nav-link:hover {
  background-color: #e9ecef;
  color: #0056b3;
}
</style>
