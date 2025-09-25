// src/router.js
import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "./stores/auth";

import Register from "./views/Register.vue";
import Verify from "./views/Verify.vue";
import AdminLogin from "./views/AdminLogin.vue";
import Participants from "./views/Participants.vue";
import Draw from "./views/Draw.vue";

const routes = [
  { path: "/", component: Register },
  { path: "/verify/:token", component: Verify, props: true },

  { path: "/admin/login", component: AdminLogin },

  
  { path: "/admin/participants", component: Participants, meta: { requiresAuth: true } },
  { path: "/admin/draw", component: Draw, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Guard global
router.beforeEach((to, _from, next) => {
  const auth = useAuthStore();
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next("/admin/login");
  } else {
    next();
  }
});

export default router;
