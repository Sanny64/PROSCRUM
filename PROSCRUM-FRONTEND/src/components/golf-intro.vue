<script setup lang="ts">
import { playSound } from '../composables/playSound.ts'
import { onMounted, ref } from 'vue'

const clubAnimation = ref('')
const ballAnimation = ref('')

function startAnimation() {
  console.log('startAnimation')
  clubAnimation.value = 'golf_club_animation'
  ballAnimation.value = 'golf_ball_animation'
  setTimeout(() => {
    clubAnimation.value = ''

    console.log('stopAnimation')
  }, 5000)
  setTimeout(() => {
    ballAnimation.value = ''
    console.log('stopAnimation')
  }, 5000)
  setTimeout(() => {
    console.log('stopAnimation')
    playSound()
  }, 3500)
}
</script>

<template>
  <div class="golf_intro">
    <div class="golf_background"><img src="../assets/Intro/GolfIntroPlatz.png" /></div>
    <div class="golf_object golf_club">
      <img
        src="../assets/Intro/GolfIntroSchlaeger.png"
        @click="startAnimation"
        :class="clubAnimation"
      />
    </div>
    <div class="golf_object golf_ball">
      <img src="../assets/Intro/GolfIntroBall.png" :class="ballAnimation" />
    </div>
  </div>
</template>

<style scoped>
@import '../style/golf-intro.css';
</style>
