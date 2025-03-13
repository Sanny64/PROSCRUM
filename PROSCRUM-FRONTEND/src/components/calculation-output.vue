<script setup lang="ts">
import {inject, type Ref, ref, watch, watchEffect} from 'vue'
import RoundsChart from '@/components/rounds-chart.vue'
import type {Round, User } from '../types/types.ts'
import RoundsTable from '@/components/rounds-table.vue'

import { useI18n } from 'vue-i18n'

const activeUserAPI = inject<Ref<User | 'INVALID'>>("activeUser", ref("INVALID"));



const { t } = useI18n()

const props = defineProps<{
  pollingStatus: number | undefined
  roundsResult: Round[]
}>()

let calc_result_2020 = ref<number | undefined>()
let calc_result_2021 = ref<number | undefined>()



watchEffect(() => {
  if (props.roundsResult.length > 0) {
    calc_result_2020.value = props.roundsResult[props.roundsResult.length - 1].calc_result_2020
    calc_result_2021.value = props.roundsResult[props.roundsResult.length - 1].calc_result_2021
  }
})
</script>

<template>
  <div class="component-right">
    <div class="headline">
      <div v-if="props.pollingStatus === 199" class="loadingGif">
        <img src="../assets/loading-gif.gif" alt="loading-gif" />
      </div>
      <h1 >{{ t('output.output') }}</h1>
    </div>
    <div class="hdcInfo">
      <h2 v-if="activeUserAPI != 'INVALID'">{{ t('output.yourCurrentHandicap') }} {{activeUserAPI.first_name}} {{activeUserAPI.last_name}}:</h2>

      <div class="calcOutput">
        <i>{{ t('output.until2021') }}</i>
        <b>{{ calc_result_2020 }}</b>
      </div>

      <div class="calcOutput">
        <i>{{ t('output.from2021') }}</i>
        <b>{{ calc_result_2021 }}</b>
      </div>
    </div>

    <div v-if="props.roundsResult.length > 0" class="roundsInfo">
      <rounds-chart :rounds-data="props.roundsResult"></rounds-chart>
      <rounds-table :rounds-data="props.roundsResult"></rounds-table>
    </div>
  </div>
</template>

<style scoped>
@import '../style/calculation-output.css';
</style>
