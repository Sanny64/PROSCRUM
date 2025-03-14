<script setup lang="ts">
import {defineEmits, inject, reactive, type Ref, ref, watch, watchEffect} from 'vue'
import RoundsChart from '@/components/rounds-chart.vue'
import type {Course, getScorecard, Round, User} from '../types/types.ts'
import RoundsTable from '@/components/rounds-table.vue'

import { useI18n } from 'vue-i18n'

const activeUserAPI = inject<Ref<User | 'INVALID'>>("activeUser", ref("INVALID"));

const { t } = useI18n()

const props = defineProps<{
  courseList: Course[]
}>()

console.log('CourseList: ', props.courseList)

// Ausgewählte Option
const selectedCourseName = ref<string | null>('')
const selectedCourse = ref<Course>()
const selectedCourseID = ref<number>()
const isDropdownOpen = ref(false)
const HDC = ref<number | undefined>(54)

// Funktion zum Umschalten des Dropdown-Menüs
const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value
}

// Funktion zum Auswählen einer Option
const selectCourse = (course: Course) => {
  selectedCourse.value = course
  selectedCourseName.value = course.course_name
  selectedCourseID.value = course.course_id
  isDropdownOpen.value = false // Menü schließen
}

const Scorecard = reactive<getScorecard>({
  HDC: undefined,
  course_id: undefined,
})

watchEffect(() => {
  Scorecard.HDC = HDC.value

  Scorecard.course_id = selectedCourseID.value
})

const inputInfo = ref('')

const emit = defineEmits(['Scorecard'])

const btnScorecard = () => {

  let nullFormDate = JSON.parse(JSON.stringify(Scorecard))

  if (selectedCourseName.value === '') {
    console.log('Bitte wählen Sie einen Golfplatz')
  } else if (nullFormDate) {
    inputInfo.value = ''
    console.log('Emit gesendet: ', nullFormDate)
    emit('Scorecard', nullFormDate)
  } else {
    console.log('Bitte geben Sie einen Wert ein')
    inputInfo.value = 'Bitte geben Sie einen Wert ein'
  }
}
</script>

<template>
  <div class="component-right">
    <div class="headline">
      <h1 >{{ t('scorecard.input')}}</h1>
    </div>

    <div class="infoBox" v-if="inputInfo">
      <p>{{ inputInfo }}</p>
    </div>

    <div class="form-group">
        <label for="HDC">{{ t('scorecard.inputHDC') }}</label>
        <input
          type="number"
          v-model="HDC"
          id="HDC"
          required
        />
    </div>

    <form @submit.prevent="btnScorecard">
    <!-- Dropdown -->
      <div class="dropdown">
        <button type="button" class="dropdown-button" @click="toggleDropdown">
          {{ selectedCourseName || t('input.courseSelection') }}
        </button>
        <ul
          v-if="isDropdownOpen"
          class="dropdown-menu"
          :class="{ 'multi-column': courseList.length > 10 }"
        >
          <li
            v-if="courseList"
            v-for="course in courseList"
            :key="course.course_id"
            @click="selectCourse(course)"
            @keydown.enter.prevent="selectCourse(course)"
            class="dropdown-item"
            tabindex="0"
          >
            {{ course.course_name }}
          </li>
        </ul>
      </div>
      <div  v-if="selectedCourse">
      <div class="form-group" >
        <label for="courseRating">{{ t('input.courseRating_all') }}</label>
        <b>{{ selectedCourse?.course_rating_all }}</b>
        </div>
      <div class="form-group" >
          <label for="courseRating">{{ t('input.course_par_all') }}</label>
          <b>{{ selectedCourse?.course_par_all }}</b>
      </div>
      <div class="form-group">
        <label for="slopeRating">{{ t('input.slopeRating') }}</label>
        <b>{{ selectedCourse?.slope_rating }}</b>
      </div>
      </div>

      <!-- Löcher -->
      <div v-if="selectedCourse" class="holes-container">
        <div class="hole" v-for="(score, index) in 18" :key="index">
          <b :for="'hole-' + (index)">{{ index + 1}}{{ t('input.hole') }}</b>
          <label>{{ t('input.par') }}</label>
          <b>{{selectedCourse?.holes[index].par }}</b>
          <label >{{ t('input.hdc') }}</label>
          <b>{{selectedCourse?.holes[index].hdc }}</b>
        </div>
      </div>

      <!-- Absenden -->
      <button v-if="selectedCourse" type="submit" class="submit-btn">{{ t('scorecard.calculate') }}</button>
    </form>
  </div>
</template>

<style scoped>
@import '../style/score-card.css';
</style>
