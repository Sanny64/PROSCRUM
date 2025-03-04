<template>
  <div id="app">
    <nav-bar></nav-bar>
    <router-view></router-view>
    <!--    <golf-intro v-if="onMountedBoolean"></golf-intro>-->
  </div>
</template>

<script setup lang="ts">
import NavBar from '@/components/nav-bar.vue'
// import GolfIntro from "@/components/golf-intro.vue";
import { onMounted, ref } from 'vue'
// import HomePage from "@/pages/HomePage.vue";

let onMountedBoolean = ref(false)

onMounted(() => {
  onMountedBoolean.value = true
  console.log('onMountedBoolean: ', onMountedBoolean)
  setTimeout(() => {
    console.log('onMountedBoolean im Time:  ', onMountedBoolean)
    onMountedBoolean.value = false
  }, 6000)
})
</script>

<style>
@import '../style/main.css';
</style>
