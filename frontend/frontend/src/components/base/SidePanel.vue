<template>
    <div class="sidebar">
      <ul>
        <li><a :href="'/wall/'+userID">Мой профиль</a></li>
        <li><a href="#feed">Лента</a></li>
        <li><a :href="'/friends/'">Друзья</a></li>
        <li><a href="#messages">Сообщения</a></li>
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
    background-color: #f8f9fa;
    padding: 20px;
    box-shadow: 2px 0 5px rgba(0,0,0,0.1);
    height: 100vh;
  }
  .sidebar ul {
    list-style-type: none;
    padding: 0;
  }
  .sidebar li {
    margin: 10px 0;
  }
  .sidebar a {
    text-decoration: none;
    color: #333;
    font-weight: bold;
  }
  .sidebar a:hover {
    color: #007bff;
  }
  </style>
  