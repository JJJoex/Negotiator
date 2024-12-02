import { createWebHistory, createRouter } from 'vue-router';
import Introduction from './pages/Introduction.vue';
import Preparation from './pages/Preparation.vue';
import Bidding from './pages/Bidding.vue';
import Finish from './pages/Finish.vue';

const routes = [
  { path: '/description', component: Introduction },
  { path: '/preparation', component: Preparation },
  { path: '/negotiation', component: Bidding },
  { path: '/finish', component: Finish },
  { path: '/', redirect: '/description' }, // 默认重定向到 Description
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
