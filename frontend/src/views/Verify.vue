<template>
  <div class="container mt-5">
    <h2>Verificación de correo</h2>
    <div v-if="step === 'verify'">
      <p>{{ message }}</p>
      <form @submit.prevent="setPassword">
        <div class="mb-3">
          <label>Contraseña</label>
          <input v-model="password" type="password" class="form-control" required />
        </div>
        <button class="btn btn-success">Crear contraseña</button>
      </form>
    </div>
    <p v-if="step === 'done'">{{ message }}</p>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const token = route.params.token;
const message = ref("");
const password = ref("");
const step = ref("verify");

onMounted(async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/verify/${token}/`);
    message.value = res.data.message;
  } catch {
    message.value = "Token inválido o expirado.";
    step.value = "done";
  }
});

async function setPassword() {
  try {
    const res = await axios.post("http://127.0.0.1:8000/api/set-password/", {
      token,
      password: password.value,
    });
    message.value = res.data.message;
    step.value = "done";
  } catch {
    message.value = "Error al crear contraseña.";
  }
}
</script>
