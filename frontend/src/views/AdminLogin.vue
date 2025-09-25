<template>
  <div class="container mt-5">
    <h2>Login Administrador</h2>
    <form @submit.prevent="login">
      <div class="mb-3">
        <label>Usuario</label>
        <input v-model="username" type="text" class="form-control" required />
      </div>
      <div class="mb-3">
        <label>Contraseña</label>
        <input v-model="password" type="password" class="form-control" required />
      </div>
      <button class="btn btn-primary">Ingresar</button>
    </form>
    <p v-if="error" class="text-danger mt-3">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "../stores/auth";
import { useRouter } from "vue-router";

const username = ref("");
const password = ref("");
const error = ref("");
const auth = useAuthStore();
const router = useRouter();

async function login() {
  try {
    await auth.login(username.value, password.value);
    router.push("/admin/participants");
  } catch {
    error.value = "Credenciales inválidas.";
  }
}
</script>
