<script setup lang="ts">
import GolfHandicapApp from '@/views/GolfHandicapApp.vue'

import { watch } from 'vue';
import { useI18n } from 'vue-i18n';

    const { t, locale } = useI18n();

    watch(locale, () => {
      document.title = t('title');
    }, { immediate: true });

</script>

<template>
  <div id="app">
    <GolfHandicapApp></GolfHandicapApp>
  </div>
</template>

<style scoped></style>
