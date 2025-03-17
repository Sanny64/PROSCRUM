<script setup lang="ts">
import {ref, defineEmits, reactive, watchEffect, onMounted, inject, type Ref} from 'vue'
import type {FormData, Course, Round, User} from '../types/types.ts'
import { useI18n } from 'vue-i18n'
import {apiCallUser} from "@/composables/api-call-user.ts";

const activeUserAPI = inject<Ref<User | 'INVALID'>>("activeUser", ref("INVALID"));



const { t } = useI18n()

let length = ref(18)
let lengthStart = ref(0)
let isChecked = ref(true)

const props = defineProps<{
  courseList: Course[]
  lastRound: Round[]
}>()





console.log('CourseList: ', props.courseList)
console.log('lastRound: ', props.lastRound)
// Ausgewählte Option
let min_date = "1980-01-01"
if (props.lastRound) {
  min_date = props.lastRound[props.lastRound.lenght - 1].date
}
const selectedCourseName = ref<string | null>('')
const selectedCourse = ref<Course>()
const isDropdownOpen = ref(false)
const selectedDate = ref<string>('') // Reaktiver Wert für das Datum
const selectedRatingOption = ref<'all' | '1to9' | '10to18'>('all')

// Funktion zum Umschalten des Dropdown-Menüs
const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value
}

// Funktion zum Auswählen einer Option
const selectCourse = (course: Course) => {
  selectedCourseName.value = course.course_name
  selectedCourse.value = course
  isDropdownOpen.value = false // Menü schließen
}
const formData = reactive<FormData>({
  round_number: undefined,
  date: undefined,
  course: undefined,
  user_id: activeUserAPI.value.user_id || 0,
  user: activeUserAPI.value,
  scores: [], // Initialisiertes Array
})

watchEffect(() => {
  formData.course = selectedCourse.value

  formData.round_number = props.lastRound.length + 1
})

// WatchEffect, um die Länge und Zufallswerte dynamisch zu setzen
watchEffect(() => {
  formData.scores = Array.from(
    { length: 18 },
    () => Math.floor(Math.random() * (10 - 1 + 1)) + 1, // Zufallszahlen zwischen 1 und 10
  )
})

watchEffect(() => {
  if (selectedDate.value) {
    formData.date = new Date(selectedDate.value).toISOString().split('T')[0] // ISO-Format ohne Zeit
  }
})


watchEffect(() => {
  // Länge der Löcher basierend auf dem Zustand setzen
  if (selectedRatingOption.value === '1to9' ) {
    length.value = 9
    lengthStart.value = 1
    console.log('Checkbox aktiviert. Länge: ' + length.value)
  }else if(selectedRatingOption.value === '10to18'){
    length.value = 9
    lengthStart.value = 10

  }else {
    lengthStart.value = 1
    length.value = 18
    console.log('Checkbox deaktiviert. Länge: ' + length.value)

  }
});

const inputInfo = ref('')

const emit = defineEmits(['formData'])

const btnCalculation = () => {

  let nullFormDate = JSON.parse(JSON.stringify(formData))

  if (selectedRatingOption.value === '1to9' ) {

    for (let i = 9; i <= 17; i++) {
      nullFormDate.scores[i] = 0;
    }
  }else if(selectedRatingOption.value === '10to18'){

    for (let i = 0; i <= 8; i++) {
      nullFormDate.scores[i] = 0;
    }

  }


  if (selectedCourseName.value === '') {
    console.log('Bitte wählen Sie einen Golfplatz')
  } else if (nullFormDate) {
    inputInfo.value = ''
    console.log('Emit gesendet: ', nullFormDate)
    emit('formData', nullFormDate)
  } else {
    console.log('Bitte geben Sie einen Wert ein')
    inputInfo.value = 'Bitte geben Sie einen Wert ein'
  }
}
</script>

<template>

  <div class="component-left">
    <div class="headline">
      <h1 >{{ t('input.input')}}</h1>
    </div>

    <div class="infoBox" v-if="inputInfo">
      <p>{{ inputInfo }}</p>
    </div>
    <form @submit.prevent="btnCalculation">
      <div class="form-group">
        <label for="round">{{ t('input.round') }}</label>
        <b>{{ formData.round_number }}</b>
      </div>
      <div class="datePicker ">
        <label for="date">{{ t('input.date') }}</label>
        <input
          type="date"
          v-model="selectedDate"
          :min="min_date"
          id="date"
          required
        />
      </div>
      <div  v-if="selectedCourse">
      <div v-if="selectedRatingOption === '1to9'">
      <div class="form-group">
        <label for="courseRating">{{ t('input.courseRating_1to9') }}</label>

        <b>{{ selectedCourse?.course_rating_1_to_9 }}</b>
        </div>
      </div>
      <div v-if="selectedRatingOption === '10to18'">
      <div class="form-group">
        <label for="courseRating">{{ t('input.courseRating_10to18') }}</label>

        <b>{{ selectedCourse?.course_rating_10_to_18 }}</b>
        </div>
      </div>
      <div v-if="selectedRatingOption === 'all'">
      <div class="form-group" >
        <label for="courseRating">{{ t('input.courseRating_all') }}</label>
        <b>{{ selectedCourse?.course_rating_all }}</b>
        </div>
      </div>
      <div v-if="selectedRatingOption === '1to9'">
        <div class="form-group">
          <label for="courseRating">{{ t('input.course_par_1to9') }}</label>

          <b>{{selectedCourse?.course_par_1_to_9 }}</b>
        </div>
      </div>
      <div v-if="selectedRatingOption === '10to18'">
        <div class="form-group">
          <label for="courseRating">{{ t('input.course_par_10to18') }}</label>

          <b>{{ selectedCourse?.course_par_10_to_18 }}</b>
        </div>
      </div>
      <div v-if="selectedRatingOption === 'all'">
        <div class="form-group" >
          <label for="courseRating">{{ t('input.course_par_all') }}</label>
          <b>{{ selectedCourse?.course_par_all }}</b>
        </div>
      </div>


      <div class="form-group">
        <label for="slopeRating">{{ t('input.slopeRating') }}</label>
        <b>{{ selectedCourse?.slope_rating }}</b>
      </div>
      </div>
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

      <!-- Switch -->
      <div v-if="selectedCourse" class="holesHeadline">
              <label>{{ t('input.courseHoleSelection') }}</label>
              <div class="radio-group">
                <label v-if="selectedCourse?.course_rating_1_to_9" class="radio-button">
                  <input  type="radio" value="1to9" v-model="selectedRatingOption" />{{t('input.courseSelection_1to9')}}
                </label>
                <label v-if="selectedCourse?.course_rating_10_to_18" class="radio-button" >
                  <input  type="radio" value="10to18" v-model="selectedRatingOption" />{{t('input.courseSelection_10to18')}}
                </label>
                <label v-if="selectedCourse?.course_rating_all" class="radio-button">
                  <input  type="radio" value="all" v-model="selectedRatingOption"  />{{t('input.courseSelection_all')}}
                </label>
              </div>

            </div>

      <!-- Löcher -->
      <div v-if="selectedCourse" class="holes-container">
        <div class="hole" v-for="(score, index) in length" :key="index">
          <b :for="'hole-' + (index)">{{ index + lengthStart}}{{ t('input.hole') }}</b>
          <label >{{ t('input.shots') }}</label>
          <input
            type="number"
            :id="'hole-' + (index + lengthStart -1)"
            v-model="formData.scores[index + lengthStart -1]"
            min="1"
            required
          />
          <label>{{ t('input.par') }}</label>
          <b>{{formData.course?.holes[index + lengthStart -1].par }}</b>
          <label >{{ t('input.hdc') }}</label>
          <b>{{ formData.course?.holes[index + lengthStart -1].hdc }}</b>
        </div>
      </div>

      <!-- Absenden -->
      <button v-if="selectedCourse" type="submit" class="submit-btn">{{ t('input.calculate') }}</button>
    </form>
  </div>
</template>

<style scoped>
@import '../style/calculation-input.css';
</style>
