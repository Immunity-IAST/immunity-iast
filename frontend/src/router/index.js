import {createRouter, createWebHistory} from 'vue-router';
import ApplicationView from '../views/ApplicationView.vue';
import DatasetView from '../views/DatasetView.vue';

const routes = [
  {
    path: '/',
    name: 'application',
    component: ApplicationView,
    meta: {requiresAuth: true},
  },
  {
    path: '/dataset',
    name: 'dataset',
    component: DatasetView,
    meta: {requiresAuth: true},
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


export default router;
