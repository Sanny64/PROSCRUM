<template>
  <div id="app">
    <nav-bar></nav-bar>
    <router-view></router-view>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import NavBar from '@/components/nav-bar.vue'
import { apiCallUser } from "@/composables/api-call-user.ts";
import {provide, onMounted, ref, type Ref} from "vue";
import type { User } from '../types/types.ts'
const { getActiveUserAPI, activeUserAPI } = apiCallUser();
let onMountedBoolean = ref(false)

const router = useRouter();
provide<Ref<User | 'INVALID'>>("activeUser", activeUserAPI);
provide<() => Promise<void>>("refreshActiveUser", getActiveUserAPI);

onMounted(async () => {
  await getActiveUserAPI();
  if(activeUserAPI.value === 'INVALID') {
    await router.push("/login");
  }else {
    await router.push("/course");
  }
})
</script>

<style>
@import '../style/main.css';
</style>
