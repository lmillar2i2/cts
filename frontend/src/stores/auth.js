// src/stores/auth.js
import { defineStore } from "pinia";
import axios from "axios";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token") || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(username, password) {
      const res = await axios.post("http://127.0.0.1:8000/api/admin/login/", {
        username,
        password,
      });
      this.token = res.data.access;
      localStorage.setItem("token", this.token);   
    },
    logout() {
      this.token = null;
      localStorage.removeItem("token");
    },
  },
});
