<script setup lang="ts">
import {inject, type Ref, ref, watch, watchEffect} from 'vue'
import RoundsChart from '@/components/rounds-chart.vue'
import type {Round, User } from '../types/types.ts'
import RoundsTable from '@/components/rounds-table.vue'

import { useI18n } from 'vue-i18n'

const activeUserAPI = inject<Ref<User | 'INVALID'>>("activeUser", ref("INVALID"));


</script>

<template>
  <div class="component-right">

  </div>
</template>

<style scoped>
@import '../style/score-card.css';
</style>
