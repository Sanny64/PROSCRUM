<script setup lang="ts">
import { nextTick, onMounted, reactive, ref, watch } from 'vue'
import type {Round, User} from '../types/types.ts'
import CalculationOutput from '@/components/calculation-output.vue'
import { apiCallInlineResponse } from '@/composables/api-call-inline-response.ts'
import { apiCallRounds } from '@/composables/api-call-rounds.ts'
import { apiCallUser } from '@/composables/api-call-user.ts'

import GolfUser from '@/components/golf-user.vue'
import RoundsFilter from '@/components/rounds-filter.vue'
import ScoreCard from "@/components/score-card.vue";
import {apiCallCourses} from "@/composables/api-call-courses.ts";

const {apiStatus, sendFormdata } = apiCallInlineResponse()
const {apiResultRounds, getRoundsAPI, updateRoundAPI } = apiCallRounds()
const {getUserAllAPI, allUserList} = apiCallUser()
const { apiResultCourse, getCoursesAPI } = apiCallCourses()


const dataTree = reactive(apiResultRounds)
const roundsList = apiResultRounds
const userList = allUserList

const inputValue = ref<string>('')
const numberValue = ref<number>()
const dateRange = ref<{ start: string, end: string }>({ start: '', end: '' }) //<---

const filteredUsersList = ref<User[]>([])



async function updateRound(round: Round) {
  console.log('Update Round: ')
  await updateRoundAPI(round) // Warten, bis der API-Aufruf abgeschlossen ist
  await nextTick() // Warten auf den nächsten DOM-Tick oder reaktive Updates
  await getRoundsAPI() // Danach die Kurse erneut abrufen
}

function filterCourses() {

  filteredUsersList.value = userList.value.filter((user: User) =>
    user.first_name.toLowerCase().includes(inputValue.value.toLowerCase())||
    user.last_name.toLowerCase().includes(inputValue.value.toLowerCase())
  )


  if (numberValue.value) {
    filteredUsersList.value = userList.value.filter(
      (user:User) => user.user_id == numberValue.value,
    )
  }

  if (dateRange.value.start && dateRange.value.end) { //<---

    filteredUsersList.value = userList.value.filter((user: User) => {
      const roundDate = new Date(user.created_at).toISOString().split('T')[0]
      return roundDate >= dateRange.value.start && roundDate <= dateRange.value.end //<---
    })
  }
}

watch([roundsList,userList, inputValue, numberValue, dateRange], filterCourses, { deep: true }) //<---

function textValueFunc(textValue: string) {
  inputValue.value = textValue
}

function numberValueFunc(number: number) {
  numberValue.value = number
}



function dateRangeFunc(range: { start: string, end: string }) {
  dateRange.value = range
}


onMounted(() => {
  getRoundsAPI()
  getUserAllAPI()
  getCoursesAPI()
})
</script>
<template>
  <div class="content">
    <div>

      <div class="filterGrid">
        <rounds-filter
          @number-value="numberValueFunc"
          @text-value="textValueFunc"
          @date-range-value="dateRangeFunc"
          :rounds-list="roundsList"
        ></rounds-filter>
      </div>

      <div class="grid">
        <div v-for="(users, index) in filteredUsersList" :key="users.user_id">
          <golf-user :user="users"  @updated-round="updateRound" :rounds-list="roundsList"></golf-user>
        </div>
      </div>
    </div>
    <score-card
      :course-list="apiResultCourse"
    ></score-card>
  </div>
</template>

<style scoped>
@import '../style/RoundsPage.css';
</style>
