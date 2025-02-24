<script setup lang="ts">
import GolfIntro from "@/components/golf-intro.vue";
import {playSound, playGolfMusic, stopGolfMusic} from "../composables/playSound.ts";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faGear } from '@fortawesome/free-solid-svg-icons';

import { ref } from 'vue';

import { useI18n } from 'vue-i18n';


const { locale, t} = useI18n();

const changeLanguage = (lang:string) => {
  locale.value = lang;
};

let settingsOpen = ref(false);
let isMuted = ref(true);

const toggleSettings = () => {
  settingsOpen.value = !settingsOpen.value;
};

function handleMusic() {
  if (isMuted.value) {
    stopGolfMusic();
  } else {
    playGolfMusic();
  }
}

</script>

<template>
  <nav class="menu-container">
    <!-- burger menu -->
    <input type="checkbox" aria-label="Toggle menu" />
    <span></span>
    <span></span>
    <span></span>

    <!-- logo -->
    <router-link to="/" class="menu-logo">
      <img src="../assets/logo.png" alt="Golf Handicap Rechner"/>
    </router-link>
    <p class="menu-headline">{{ t('title') }}</p>
    <!-- menu items -->
    <div class="menu">
      <ul>
        <li class="golf-flagg">
          <img src="../assets/golfFlagg.png" alt="Golf Handicap Rechner" @click="playSound"/>
        </li>
        <li >
          <router-link to="/">{{t('home')}}</router-link>
        </li>
        <li >
          <router-link to="/course">{{t('course')}}</router-link>
        </li>
        <li>
          <router-link to="/rounds">{{t('rounds')}}</router-link>
        </li>

      </ul>
      <ul>
        <li>
          <router-link to="/signup">{{t('signup')}}</router-link>
        </li>
        <li>
          <router-link to="/login">{{t('login')}}</router-link>
        </li>
        <li>
          <svg xmlns="http://www.w3.org/2000/svg"   @click="toggleSettings"  width="48"  height="48"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round" :class="{ 'active': settingsOpen }" class="gear-icon icon icon-tabler icons-tabler-outline icon-tabler-settings"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M10.325 4.317c.426 -1.756 2.924 -1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543 -.94 3.31 .826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756 .426 1.756 2.924 0 3.35a1.724 1.724 0 0 0 -1.066 2.573c.94 1.543 -.826 3.31 -2.37 2.37a1.724 1.724 0 0 0 -2.572 1.065c-.426 1.756 -2.924 1.756 -3.35 0a1.724 1.724 0 0 0 -2.573 -1.066c-1.543 .94 -3.31 -.826 -2.37 -2.37a1.724 1.724 0 0 0 -1.065 -2.572c-1.756 -.426 -1.756 -2.924 0 -3.35a1.724 1.724 0 0 0 1.066 -2.573c-.94 -1.543 .826 -3.31 2.37 -2.37c1 .608 2.296 .07 2.572 -1.065z" /><path d="M9 12a3 3 0 1 0 6 0a3 3 0 0 0 -6 0" /></svg>
          <div v-if="settingsOpen" class="settings" >
            <button @click="changeLanguage('en')">English</button>
            <button @click="changeLanguage('de')">Deutsch</button>
            <button @click="changeLanguage('hs')">Hessisch</button>
            <input type="checkbox"
                   id="checkboxInput"
                   v-model="isMuted"
                   @change="handleMusic">
            <label for="checkboxInput" class="toggleSwitch">

              <div class="speaker"><svg xmlns="http://www.w3.org/2000/svg" version="1.0" viewBox="0 0 75 75">
                <path d="M39.389,13.769 L22.235,28.606 L6,28.606 L6,47.699 L21.989,47.699 L39.389,62.75 L39.389,13.769z" style="stroke:#fff;stroke-width:5;stroke-linejoin:round;fill:#fff;"></path>
                <path d="M48,27.6a19.5,19.5 0 0 1 0,21.4M55.1,20.5a30,30 0 0 1 0,35.6M61.6,14a38.8,38.8 0 0 1 0,48.6" style="fill:none;stroke:#fff;stroke-width:5;stroke-linecap:round"></path>
              </svg>
              </div>

              <div class="mute-speaker"><svg version="1.0" viewBox="0 0 75 75" stroke="#fff" stroke-width="5">
                <path d="m39,14-17,15H6V48H22l17,15z" fill="#fff" stroke-linejoin="round"></path>
                <path d="m49,26 20,24m0-24-20,24" fill="#fff" stroke-linecap="round"></path>
              </svg>
              </div>
            </label>
          </div>
        </li>

      </ul>
    </div>
  </nav>



</template>

<style>

@import "../style/nav-bar.css";
</style>
