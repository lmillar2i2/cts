<script setup>
import { useAuthStore } from "./stores/auth";
import { useRouter } from "vue-router";
import logo from "./assets/cts_turismo_logo.jpg"; 

const auth = useAuthStore();
const router = useRouter();
const logout = () => {
auth.logout();            
router.push("/admin/login"); 
};

</script>


<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light px-3">
      <router-link to="/" class="navbar-brand d-flex align-items-center">
        <img :src="logo" alt="Logo" height="40" class="me-2" />
        <span>Sorteo San Valentín</span>
      </router-link>

      <ul class="navbar-nav ms-auto">
        <li class="nav-item">
          <router-link to="/" class="nav-link">Registro</router-link>
        </li>

        <template v-if="auth.isAuthenticated">
          <li class="nav-item">
            <router-link to="/admin/participants" class="nav-link">Participantes</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/draw" class="nav-link">Sorteo</router-link>
          </li>
          <li class="nav-item">
            <button class="btn btn-link nav-link" @click="logout">Salir</button>
          </li>
        </template>

        <template v-else>
          <li class="nav-item">
            <router-link to="/admin/login" class="nav-link">Admin</router-link>
          </li>
        </template>
      </ul>
    </nav>

    <router-view />
  </div>
</template>
