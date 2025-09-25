<!-- src/views/Draw.vue -->
<template>
  <div class="container mt-5">
    <h2>Sorteo de Ganador</h2>

    <div class="mb-3">
      <button class="btn btn-success" :disabled="loading" @click="draw">
        {{ loading ? "Sorteando..." : "Realizar sorteo" }}
      </button>
      <button class="btn btn-secondary ms-2" @click="goParticipants">Ver participantes</button>
    </div>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-if="winner" class="alert alert-info mt-3">
      <h4>Ganador:</h4>
      <p>{{ winner.participant.name }} - {{ winner.participant.email }}</p>
      <small>Edición: {{ winner.valentin_version }} | Fecha: {{ new Date(winner.date_won).toLocaleString() }}</small>
    </div>
  </div>
</template>

<script setup>
import { useParticipantsStore } from "../stores/participants";
import { useAuthStore } from "../stores/auth";
import { computed, ref } from "vue";
import { useRouter } from "vue-router";

const participantsStore = useParticipantsStore();
const auth = useAuthStore();
const router = useRouter();

const winner = computed(() => participantsStore.winner);
const loading = ref(false);
const error = ref("");

async function draw() {
  error.value = "";
  if (!auth.token) return router.push("/admin/login");
  try {
    loading.value = true;
    await participantsStore.drawWinner(auth.token);
  } catch (e) {
    error.value = e?.response?.data?.detail || "No fue posible realizar el sorteo.";
  } finally {
    loading.value = false;
  }
}
const goParticipants = () => router.push("/admin/participants");
</script>
