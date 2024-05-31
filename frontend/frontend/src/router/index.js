import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView
    },
    {
      path: '/registration', // Путь к странице регистрации
      name: 'Registration',
      component: () => import('../views/Registration.vue') // Компонент регистрации
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/Login.vue')
    },
    {
      path: '/profile/create',
      name: 'CreateProfile',
      component: () => import('../views/CreateProfile.vue')
    },
    {
      path: '/wall/:UserID',
      name: 'Profile',
      component: () => import('../views/Profile.vue')
    },
    {
      path: '/profile/edit/',
      name: 'UpdateProfile',
      component: () => import('../views/UpdateProfile.vue')
    },
    {
      path: '/friends/',
      name: 'Friends',
      component: () => import('../views/Friends.vue')
    }
  ]
})

export default router
