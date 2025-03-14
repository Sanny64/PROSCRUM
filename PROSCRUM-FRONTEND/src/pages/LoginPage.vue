<script setup lang="ts">
import {inject, type Ref} from "vue";

const { setError, clearError } = useErrorController(); //<---
const { t } = useI18n()

const activeUserAPI = inject<Ref<User | 'INVALID'>>("activeUser", ref("INVALID"));
const refreshActiveUser = inject<() => Promise<void>>("refreshActiveUser");

import {apiCallLogin} from '@/composables/api-call-login.ts'

import type {LoginData, User} from '@/types/types.ts'
import {nextTick, onMounted, ref, watch} from "vue";
import {useRouter} from "vue-router";
import {useErrorController} from "@/composables/error-controller.ts";
import {useI18n} from "vue-i18n";


const router = useRouter();

const loginData: LoginData = {
  username: '',
  password: ''
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

const inputType = ref('password');

function togglePasswordVisibility() {

  if (inputType.value === 'password') {
    inputType.value = 'text';
  } else {
    inputType.value = 'password';
  }
}



</script>

<template>

  <div class="content">

    <form class="modern-form" @submit.prevent="login(loginData)">
      <div class="form-title">{{t('loginPage.login_page')}}</div>

      <div class="form-body">


        <div class="input-group">
          <div class="input-wrapper">
            <svg fill="none" viewBox="0 0 24 24" class="input-icon">
              <path
                stroke-width="1.5"
                stroke="currentColor"
                d="M3 8L10.8906 13.2604C11.5624 13.7083 12.4376 13.7083 13.1094 13.2604L21 8M5 19H19C20.1046 19 21 18.1046 21 17V7C21 5.89543 20.1046 5 19 5H5C3.89543 5 3 5.89543 3 7V17C3 18.1046 3.89543 19 5 19Z"
              ></path>
            </svg>
            <input
              required
              :placeholder="$t('loginPage.email')"
              class="form-input"
              v-model="loginData.username"
              type="email"
            />
          </div>
        </div>

        <div class="input-group">
          <div class="input-wrapper">
            <svg fill="none" viewBox="0 0 24 24" class="input-icon">
              <path
                stroke-width="1.5"
                stroke="currentColor"
                d="M12 10V14M8 6H16C17.1046 6 18 6.89543 18 8V16C18 17.1046 17.1046 18 16 18H8C6.89543 18 6 17.1046 6 16V8C6 6.89543 6.89543 6 8 6Z"
              ></path>
            </svg>
            <input
              required
              :placeholder="$t('loginPage.password')"
              class="form-input"
              v-model="loginData.password"
              :type="inputType"
            />
            <button class="password-toggle" @click="togglePasswordVisibility" type="button">
              <svg fill="none" viewBox="0 0 24 24" class="eye-icon">
                <path
                  stroke-width="1.5"
                  stroke="currentColor"
                  d="M2 12C2 12 5 5 12 5C19 5 22 12 22 12C22 12 19 19 12 19C5 19 2 12 2 12Z"
                ></path>
                <circle
                  stroke-width="1.5"
                  stroke="currentColor"
                  r="3"
                  cy="12"
                  cx="12"
                ></circle>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <button class="submit-button" type="submit">
        <span class="button-text">{{t('loginPage.login')}}</span>
        <div class="button-glow"></div>
      </button>

    </form>

  </div>

</template>

<style scoped>
@import "../style/LoginPage.css";

</style>
