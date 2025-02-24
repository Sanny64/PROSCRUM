<script setup lang="ts">

import type {Course} from "@/types/types.ts";

const emit = defineEmits(['close']);

function closeEmit() {
emit('close');
}

const props = defineProps<
  {
    infoText: String;
  }>();

</script>

<template>

  <div class="notifications-container">
    <div class="error-alert">
      <div class="flex">
        <div class="flex-shrink-0" @click="closeEmit">

          <svg aria-hidden="true" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg" class="error-svg">
            <path clip-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" fill-rule="evenodd"></path>
          </svg>
        </div>
        <div class="error-prompt-container">
          <p class="error-prompt-heading">You have not selected the Hdc correctly.(i18n)
          </p><div class="error-prompt-wrap">
          <ul class="error-prompt-list" role="list">
            <li>{{infoText}}</li>
          </ul>
        </div>
        </div>
      </div>
    </div>
  </div>

</template>

<style scoped>

@import "../style/info.css";

</style>
