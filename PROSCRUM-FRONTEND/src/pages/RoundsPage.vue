<
<script setup lang="ts">
import { nextTick, onMounted, reactive, ref, watch } from 'vue'
import GolfCourse from '@/components/golf-course.vue'
import AddGolfCourse from '@/components/add-golf-course.vue'
import type {Course, Round} from '../types/types.ts'
import { apiCallCourses } from '@/composables/api-call-courses.ts'
import CalculationOutput from '@/components/calculation-output.vue'
import CalculationInput from '@/components/calculation-input.vue'
import { apiCallInlineResponse } from '@/composables/api-call-inline-response.ts'
import { apiCallRounds } from '@/composables/api-call-rounds.ts'
import GolfRound from '@/components/golf-round.vue'
import RoundsFilter from '@/components/rounds-filter.vue'

const { apiResultCourse, getCoursesAPI, addCourseAPI, deleteCourseAPI } = apiCallCourses()
const { apiStatus, sendFormdata } = apiCallInlineResponse()
const { apiResultRounds, getRoundsAPI } = apiCallRounds()
const dataTree = reactive(apiResultRounds)
const roundsList = apiResultRounds

const inputValue = ref<string>('')
const numberValue = ref<number>()
const filteredRoundsList = ref<Round[]>([])

async function addCourse(newCourse: Course) {
  await addCourseAPI(newCourse)
  await nextTick()
  await getCoursesAPI()
}

async function deleteCourse(course: Course) {
  await deleteCourseAPI(course) // Warten, bis der API-Aufruf abgeschlossen ist
  await nextTick() // Warten auf den nächsten DOM-Tick oder reaktive Updates
  await getCoursesAPI() // Danach die Kurse erneut abrufen
}

function filterCourses() {
  filteredRoundsList.value = roundsList.value.filter((round) =>
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
  getCoursesAPI()
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
          <golf-round :rounds="rounds" @course-deleted="deleteCourse"></golf-round>
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
