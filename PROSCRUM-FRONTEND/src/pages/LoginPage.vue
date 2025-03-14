<script setup lang="ts">
import {inject, type Ref} from "vue";

const { setError, clearError } = useErrorController(); //<---

const activeUserAPI = inject<Ref<User | 'INVALID'>>("activeUser", ref("INVALID"));
const refreshActiveUser = inject<() => Promise<void>>("refreshActiveUser");

import {apiCallLogin} from '@/composables/api-call-login.ts'

import type {LoginData, User} from '@/types/types.ts'
import {nextTick, onMounted, ref, watch} from "vue";
import {useRouter} from "vue-router";
import {useErrorController} from "@/composables/error-controller.ts";


const router = useRouter();

const loginData: LoginData = {
  username: 'jan@test.de',
  password: '1234'
}




async function login(loginData: LoginData) {
  console.log("1: Login", loginData);
  await apiCallLogin(loginData);
  await refreshActiveUser?.();
  console.log("5 activeUser", activeUserAPI.value);
  if(activeUserAPI.value !== 'INVALID') {
    clearError();
    {if(activeUserAPI.value.role_id === 1) {
      await router.push("/");
    }else
      await router.push("/course");
    }}

}


function logout() {
  localStorage.setItem("activeToken", "")
  activeUserAPI.value = 'INVALID'
}



</script>

<template>
  <input type="text" v-model="loginData.username" placeholder="Email">
  <input type="password" v-model="loginData.password" placeholder="Password">
  <button @click="login(loginData)">Login</button>

<div v-if="activeUserAPI != 'INVALID'">
  <h1>User: {{activeUserAPI?.first_name}} {{activeUserAPI?.last_name}}</h1>
</div>
<div v-else>
  <h1>User: Not logged in</h1>
</div>

  <button @click="logout()">Logout</button>

</template>

<style scoped>
@import "../style/LoginPage.css";

</style>
