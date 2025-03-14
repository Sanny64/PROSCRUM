<script setup lang="ts">
import { nextTick, onMounted, reactive, ref, watch } from 'vue'
import type {Round, User, ScorecardInput, Course} from '../types/types.ts'
import CalculationOutput from '@/components/calculation-output.vue'
import { apiCallInlineResponse } from '@/composables/api-call-inline-response.ts'
import { apiCallRounds } from '@/composables/api-call-rounds.ts'
import { apiCallUser } from '@/composables/api-call-user.ts'
import { jsPDF } from 'jspdf'
import autoTable, {type RowInput} from 'jspdf-autotable'

import GolfUser from '@/components/golf-user.vue'
import RoundsFilter from '@/components/rounds-filter.vue'
import ScoreCard from "@/components/score-card.vue";
import {apiCallCourses} from "@/composables/api-call-courses.ts";
import {getScorecard} from "@/composables/api-call-scorecard.ts";

const {apiStatus, sendFormdata } = apiCallInlineResponse()
const {apiResultRounds, getRoundsAPI, updateRoundAPI } = apiCallRounds()
const {getUserAllAPI, allUserList} = apiCallUser()
const { apiResultCourse, getCoursesAPI } = apiCallCourses()
const { apiResultScorecard, getStrokesAhead} = getScorecard()


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

async function generateScorecard(input: ScorecardInput, currentCourse: Course) {
  await getStrokesAhead(input)
  await nextTick()
  generatePDF(apiResultScorecard.value.hits_ahead, currentCourse, apiResultScorecard.value.course_HDC)
}

async function generatePDF(list_s_A: number[], course: Course, course_HC: number) {
  let slashLists = list_s_A.map(value => '\\'.repeat(value));

  const pdf = new jsPDF()

  pdf.setFontSize(20);
  pdf.text('PROSCRUM Scorecard', 65, 15);
  pdf.setFontSize(16);
  pdf.text(`Course: ${course.course_name}`, 14, 35);
  pdf.setFontSize(12);
  pdf.text(`Course HC: ${course_HC}`, 14, 45)
  pdf.text('Platzparameter:', 14, 55)
  pdf.text(`Par: ${course.course_par_all}`, 50, 55)
  pdf.text(`Slope Rating: ${course.slope_rating}`, 90, 55)
  pdf.text(`Course Rating: ${course.course_rating_all}`, 150, 55)

  const tableColumns = ["Loch", "Par", "HDC", "Schläge vor", "Schläge"];
  const tableRows: RowInput[] = course.holes.map((hole, index) => [
    hole.hole ?? "", hole.par ?? 0, hole.hdc ?? 0, slashLists[index] ?? 0, ]
  )

  autoTable(pdf, {
    head: [tableColumns],
    body: tableRows,
    startY: 60,
    theme: 'grid',
    styles: {fontSize: 10, cellPadding: 2},
    headStyles: { fillColor: [22,160,133], textColor: 255}
  })

  // Das PDF als Blob erhalten
  const pdfBlob = pdf.output('blob');

  // Neue Seite im Browser mit dem PDF öffnen
  const pdfUrl = URL.createObjectURL(pdfBlob);
  const pdfWindow = window.open(pdfUrl);

  if (pdfWindow) {
    pdfWindow.document.title = 'Scorecard PDF'; // Optionale Titelanpassung
  }
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
      @Scorecard="generateScorecard"
      :course-list="apiResultCourse"
    ></score-card>
  </div>
</template>

<style scoped>
@import '../style/RoundsPage.css';
</style>
