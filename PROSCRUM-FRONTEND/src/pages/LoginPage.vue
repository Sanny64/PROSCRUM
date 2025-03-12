<script setup lang="ts">
import {apiCallUser} from "@/composables/api-call-user.ts";
const { getActiveUserAPI } = apiCallUser()

import {apiCallLogin} from '@/composables/api-call-login.ts'

import type {LoginData, User} from '@/types/types.ts'
import {nextTick, onMounted, ref, watch} from "vue";


const activeUser = ref<User | "INVALID">("INVALID")


const loginData: LoginData = {
  username: 'robin@test.de',
  password: '1234'
}

onMounted(async () => {
  activeUser.value = await getActiveUserAPI();
});


async function login(loginData: LoginData) {
  console.log("1: Login", loginData);
  await apiCallLogin(loginData); // API-Call abwarten
  activeUser.value = await getActiveUserAPI(); // Danach den Benutzer abrufen
  console.log("5 activeUser", activeUser.value);
}


function logout() {
  localStorage.setItem("activeToken", "")
    activeUser.value = 'INVALID'
}



</script>

<template>



  <input type="text" v-model="loginData.username" placeholder="Email">
  <input type="password" v-model="loginData.password" placeholder="Password">
  <button @click="login(loginData)">Login</button>

<div v-if="activeUser != 'INVALID'">
  <h1>User: {{activeUser?.first_name}} {{activeUser?.last_name}}</h1>
</div>
<div v-else>
  <h1>User: Not logged in</h1>
</div>



  <button @click="logout()">Logout</button>

</template>

<style scoped>
@import "../style/LoginPage.css";

</style>
