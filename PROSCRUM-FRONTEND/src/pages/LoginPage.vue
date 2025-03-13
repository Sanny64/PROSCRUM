<script setup lang="ts">
import { inject, type Ref } from 'vue'

const activeUserAPI = inject<Ref<User | 'INVALID'>>('activeUser', ref('INVALID'))
const refreshActiveUser = inject<() => Promise<void>>('refreshActiveUser')

import { apiCallLogin } from '@/composables/api-call-login.ts'

import type { LoginData, User } from '@/types/types.ts'
import { nextTick, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const loginData: LoginData = {
  username: 'jan@test.de',
  password: '1234',
}

async function login(loginData: LoginData) {
  console.log('1: Login', loginData)
  await apiCallLogin(loginData)
  await refreshActiveUser?.()
  console.log('5 activeUser', activeUserAPI.value)
  await router.push('/course')
}

function logout() {
  localStorage.setItem('activeToken', '')
  activeUserAPI.value = 'INVALID'
}
</script>

<template>
  <div class="main">
    <div class="wrapper">
      <div v-if="activeUserAPI != 'INVALID'">
        <h1>User: {{ activeUserAPI?.first_name }} {{ activeUserAPI?.last_name }}</h1>
      </div>
      <div v-else>
        <h1 id="title">Anmeldung</h1>
      </div>

      <div class="inputs">
        <input type="text" v-model="loginData.username" placeholder="Email" />
        <input type="password" v-model="loginData.password" placeholder="Password" />
      </div>
      <button id="loginButton" @click="login(loginData)">Login</button>
    </div>
  </div>
</template>

<style scoped>
@import '../style/LoginPage.css';
</style>
