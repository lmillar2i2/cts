<template>
  <div class="container mt-5">
    <h2>Lista de Participantes</h2>

    <div class="d-flex mb-3 gap-2">
      <button class="btn btn-secondary" @click="loadParticipants">Refrescar</button>

      <select v-model="filterVerified" class="form-select w-auto">
        <option value="all">Todos</option>
        <option value="true">Verificados</option>
        <option value="false">No verificados</option>
      </select>
    </div>

    <ul class="list-group">
      <li
        v-for="p in filteredParticipants"
        :key="p.id"
        class="list-group-item"
      >
        {{ p.name }} - {{ p.email }} - Verificado: {{ p.is_verified ? "Sí" : "No" }}

      </li>
    </ul>
  </div>
</template>

<script setup>
import { useParticipantsStore } from "../stores/participants";
import { useAuthStore } from "../stores/auth";
import { onMounted, ref, computed } from "vue";

const participantsStore = useParticipantsStore();
const auth = useAuthStore();

const filterVerified = ref("all");

const participants = computed(() => participantsStore.list);

const filteredParticipants = computed(() => {
  if (filterVerified.value === "all") return participants.value;
  const isVerified = filterVerified.value === "true";
  return participants.value.filter((p) => p.is_verified === isVerified);
});

async function loadParticipants() {
  if (auth.token) {
    await participantsStore.fetchParticipants(auth.token);
  }
}

onMounted(loadParticipants);
</script>
