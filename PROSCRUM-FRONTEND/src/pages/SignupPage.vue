<script setup lang="ts">

import RoundsChart from "@/components/rounds-chart.vue";
import type {LoginData, UserCreate} from "@/types/types.ts";
import {apiCallLogin, } from "@/composables/api-call-login.ts";
import {apiCallUser} from "@/composables/api-call-user.ts";
const { addUserAPI } = apiCallUser()
const userCreate: UserCreate = {
  email: "jakobfischer@gmail.com",
  password: "1234",
  role_id: 4,
  first_name: "Jakob",
  last_name: "Fischer"
}

async function signup(userCreate: UserCreate) {
  await addUserAPI(userCreate); // API-Call abwarten
}

</script>

<template>

  <input type="text" v-model="userCreate.first_name" placeholder="Vorname">
  <input type="text" v-model="userCreate.last_name" placeholder="Nachname">
  <input type="number" v-model="userCreate.role_id" placeholder="Role">
  <input type="text" v-model="userCreate.email" placeholder="Email">
  <input type="password" v-model="userCreate.password" placeholder="Password">

  <button @click="signup(userCreate)">Registriren</button>

</template>

<style scoped>
@import "../style/SignupPage.css";


</style>
