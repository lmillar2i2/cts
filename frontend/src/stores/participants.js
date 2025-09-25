import { defineStore } from "pinia";
import axios from "axios";

export const useParticipantsStore = defineStore("participants", {
  state: () => ({
    list: [],
    winner: null,
  }),
  actions: {
    async fetchParticipants(token) {
      const res = await axios.get("http://127.0.0.1:8000/api/admin/participants/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      this.list = res.data;
    },
    async drawWinner(token) {
      const res = await axios.post("http://127.0.0.1:8000/api/admin/draw/", {}, {
        headers: { Authorization: `Bearer ${token}` },
      });
      this.winner = res.data.winner;
    },
  },
});
