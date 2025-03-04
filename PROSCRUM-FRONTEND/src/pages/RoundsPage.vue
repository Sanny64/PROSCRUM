<
<script setup lang="ts">
import { nextTick, onMounted, reactive, ref, watch } from 'vue'
import type { Round} from '../types/types.ts'
import CalculationOutput from '@/components/calculation-output.vue'
import { apiCallInlineResponse } from '@/composables/api-call-inline-response.ts'
import { apiCallRounds } from '@/composables/api-call-rounds.ts'
import GolfRound from '@/components/golf-round.vue'
import RoundsFilter from '@/components/rounds-filter.vue'

const { apiStatus, sendFormdata } = apiCallInlineResponse()
const { apiResultRounds, getRoundsAPI, updateRoundAPI } = apiCallRounds()
const dataTree = reactive(apiResultRounds)
const roundsList = apiResultRounds

const inputValue = ref<string>('')
const numberValue = ref<number>()
const filteredRoundsList = ref<Round[]>([])



async function updateRound(round: Round) {
  console.log('Update Round: ')
  await updateRoundAPI(round) // Warten, bis der API-Aufruf abgeschlossen ist
  await nextTick() // Warten auf den nächsten DOM-Tick oder reaktive Updates
  await getRoundsAPI() // Danach die Kurse erneut abrufen
}

function filterCourses() {

  filteredRoundsList.value = roundsList.value.filter((round: Round) =>
    round.course.course_name.toLowerCase().includes(inputValue.value.toLowerCase()),
  )


  if (numberValue.value) {
    filteredRoundsList.value = filteredRoundsList.value.filter(
      (round) => round.round_number == numberValue.value,
    )
  }
}

watch([roundsList, inputValue, numberValue], filterCourses)

function textValueFunc(textValue: string) {
  inputValue.value = textValue
}

function numberValueFunc(number: number) {
  numberValue.value = number
}

onMounted(() => {
  getRoundsAPI()
})
</script>
<template>
  <div class="content">
    <div>
      <div class="filterGrid">
        <rounds-filter
          @number-value="numberValueFunc"
          @text-value="textValueFunc"
          :rounds-list="roundsList"
        ></rounds-filter>
      </div>

      <div class="grid">
        <div v-for="(rounds, index) in filteredRoundsList" :key="rounds.round_number">
          <golf-round :rounds="rounds" @updated-round="updateRound"></golf-round>
        </div>
      </div>
    </div>

    <calculation-output
      :polling-status="apiStatus"
      :rounds-result="apiResultRounds"
    ></calculation-output>
  </div>
</template>

<style scoped>
@import '../style/RoundsPage.css';
</style>
