<template>
  <div class="container mt-5">
    <h2>Registro al Sorteo</h2>
    <form @submit.prevent="register">
      <div class="mb-3">
        <label>Nombre</label>
        <input v-model="name" type="text" class="form-control" required />
        <div v-if="errors.name" class="text-danger mt-1">
          {{ errors.name }}
        </div>
      </div>
      <div class="mb-3">
        <label>Email</label>
        <input v-model="email" type="email" class="form-control" required />
        <div v-if="errors.email" class="text-danger mt-1">
          {{ errors.email }}
        </div>
      </div>
      <div class="mb-3">
        <label>Teléfono</label>
        <input v-model="phone" type="text" class="form-control" />
        <div v-if="errors.phone" class="text-danger mt-1">
          {{ errors.phone }}
        </div>
      </div>
      <button class="btn btn-primary" :disabled="loading">
        <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
        {{ loading ? "Registrando..." : "Registrar" }}
      </button>
    </form>
    <p v-if="message" class="alert alert-info mt-3">{{ message }}</p>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref } from "vue";

const name = ref("");
const email = ref("");
const phone = ref("");
const message = ref("");
const loading = ref(false);
const errors = ref({});

async function register() {
  loading.value = true;
  message.value = "";
  errors.value = {};
  try {
    const res = await axios.post("http://127.0.0.1:8000/api/register/", {
      name: name.value,
      email: email.value,
      phone: phone.value,
    });
    message.value = res.data.message;
  } catch (err) {
    if (err.response?.data) {
      errors.value = err.response.data; 
      message.value = err.response.data.detail || "";
    } else {
      message.value = "Error en registro";
    }
  } finally {
    loading.value = false;
  }
}
</script>
