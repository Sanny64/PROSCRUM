<template>
  <div id="app">
    <nav-bar></nav-bar>
    <router-view></router-view>
    <error-handling :info-text="errorText"></error-handling>  <!-- <--- Direkt aus errorText -->

  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import NavBar from '@/components/nav-bar.vue'
import { apiCallUser } from "@/composables/api-call-user.ts";
import { useErrorController, errorText } from "@/composables/error-controller.ts";
import { provide, onMounted, ref, type Ref } from "vue";
import type { User } from '../types/types.ts'
import ErrorHandling from "@/components/error-handling.vue";
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const { getActiveUserAPI, activeUserAPI } = apiCallUser();
let onMountedBoolean = ref(false)

const { setError, clearError } = useErrorController(); //<---

const router = useRouter();
provide<Ref<User | 'INVALID'>>("activeUser", activeUserAPI);
provide<() => Promise<void>>("refreshActiveUser", getActiveUserAPI);


onMounted(async () => {
  await getActiveUserAPI();
  if(activeUserAPI.value === 'INVALID') {
    setError(t('error.login.login'));
    await router.push("/login");
  } else {

    if(activeUserAPI.value.role_id === 1) {
      await router.push("/");
    } else {
      await router.push("/course");
    }
  }
});
</script>


<style>
@import '../style/main.css';
</style>
