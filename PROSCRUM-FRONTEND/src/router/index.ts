import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../pages/HomePage.vue';
import SignupPage from '../pages/SignupPage.vue';
import CoursePage from "@/pages/CoursePage.vue";
import RoundsPage from "@/pages/RoundsPage.vue";
import LoginPage from "@/pages/LoginPage.vue";


const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/course',
    name: 'Course',
    component: CoursePage,
  },
  {
    path: '/rounds',
    name: 'Rounds',
    component: RoundsPage,
  },
  {
    path: '/signup',
    name: 'Signup',
    component: SignupPage,
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

export default router;
