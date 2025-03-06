<script setup lang="ts">
import { ref, defineEmits, reactive, watchEffect } from 'vue'
import type { FormData, Course } from '../types/types.ts'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

let length = ref(18)
let lengthStart = ref(0)
let isChecked = ref(true)

const props = defineProps<{
  courseList: Course[]
}>()

props.courseList.push( {
  course_id: 1,
  course_name: "Platz am See",
  course_par_1_to_9: null,
  course_par_10_to_18: null,
  course_par_all: 72,
  course_rating_1_to_9: null,
  course_rating_10_to_18: null,
  course_rating_all: 72.3,
  slope_rating: 130,
  holes: [
    { hole: 1, par: 3, hdc: 16 },
    { hole: 2, par: 4, hdc: 1 },
    { hole: 3, par: 4, hdc: 10 },
    { hole: 4, par: 5, hdc: 7 },
    { hole: 5, par: 4, hdc: 13 },
    { hole: 6, par: 4, hdc: 4 },
    { hole: 7, par: 3, hdc: 17 },
    { hole: 8, par: 4, hdc: 2 },
    { hole: 9, par: 4, hdc: 11 },
    { hole: 10, par: 5, hdc: 8 },
    { hole: 11, par: 4, hdc: 14 },
    { hole: 12, par: 4, hdc: 5 },
    { hole: 13, par: 3, hdc: 18 },
    { hole: 14, par: 4, hdc: 3 },
    { hole: 15, par: 4, hdc: 12 },
    { hole: 16, par: 5, hdc: 9 },
    { hole: 17, par: 4, hdc: 15 },
    { hole: 18, par: 4, hdc: 6 }
  ]
}, {
  course_id: 2,
  course_name: "Leichte Prise",
  course_par_1_to_9: 30,
  course_par_10_to_18: null,
  course_par_all: 72,
  course_rating_1_to_9: 40,
  course_rating_10_to_18: null,
  course_rating_all: 72.3,
  slope_rating: 130,
  holes: [
    { hole: 1, par: 3, hdc: 16 },
    { hole: 2, par: 4, hdc: 1 },
    { hole: 3, par: 4, hdc: 10 },
    { hole: 4, par: 5, hdc: 7 },
    { hole: 5, par: 4, hdc: 13 },
    { hole: 6, par: 4, hdc: 4 },
    { hole: 7, par: 3, hdc: 17 },
    { hole: 8, par: 4, hdc: 2 },
    { hole: 9, par: 4, hdc: 11 },
    { hole: 10, par: 5, hdc: 8 },
    { hole: 11, par: 4, hdc: 14 },
    { hole: 12, par: 4, hdc: 5 },
    { hole: 13, par: 3, hdc: 18 },
    { hole: 14, par: 4, hdc: 3 },
    { hole: 15, par: 4, hdc: 12 },
    { hole: 16, par: 5, hdc: 9 },
    { hole: 17, par: 4, hdc: 15 },
    { hole: 18, par: 4, hdc: 6 }
  ]
}, {
  course_id: 3,
  course_name: "Schwerer Brocken",
  course_par_1_to_9: 10,
  course_par_10_to_18: 15,
  course_par_all: 72,
  course_rating_1_to_9: 20,
  course_rating_10_to_18: 30,
  course_rating_all: 72.3,
  slope_rating: 130,
  holes: [
    { hole: 1, par: 3, hdc: 16 },
    { hole: 2, par: 4, hdc: 1 },
    { hole: 3, par: 4, hdc: 10 },
    { hole: 4, par: 5, hdc: 7 },
    { hole: 5, par: 4, hdc: 13 },
    { hole: 6, par: 4, hdc: 4 },
    { hole: 7, par: 3, hdc: 17 },
    { hole: 8, par: 4, hdc: 2 },
    { hole: 9, par: 4, hdc: 11 },
    { hole: 10, par: 5, hdc: 8 },
    { hole: 11, par: 4, hdc: 14 },
    { hole: 12, par: 4, hdc: 5 },
    { hole: 13, par: 3, hdc: 18 },
    { hole: 14, par: 4, hdc: 3 },
    { hole: 15, par: 4, hdc: 12 },
    { hole: 16, par: 5, hdc: 9 },
    { hole: 17, par: 4, hdc: 15 },
    { hole: 18, par: 4, hdc: 6 }
  ]
})

console.log('CourseList: ', props.courseList)

// Ausgewählte Option
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
  scores: [], // Initialisiertes Array
})

watchEffect(() => {
  formData.course = selectedCourse.value
})

// WatchEffect, um die Länge und Zufallswerte dynamisch zu setzen
watchEffect(() => {
  formData.scores = Array.from(
    { length: 18 },
    // () => Math.floor(Math.random() * (10 - 1 + 1)) + 1, // Zufallszahlen zwischen 1 und 10
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

  console.log('Emit gesendet: ', nullFormDate)

  // if (selectedCourseName.value === '') {
  //   console.log('Bitte wählen Sie einen Golfplatz')
  // } else if (formData) {
  //   inputInfo.value = ''
  //   console.log('Emit gesendet: ', formData)
  //   emit('formData', formData)
  // } else {
  //   console.log('Bitte geben Sie einen Wert ein')
  //   inputInfo.value = 'Bitte geben Sie einen Wert ein'
  // }
}
</script>

<template>
  <div class="component-left">
    <div class="headline">
      <h1>{{ t('input.input') }}</h1>
    </div>

    <div class="infoBox" v-if="inputInfo">
      <p>{{ inputInfo }}</p>
    </div>
    <form @submit.prevent="btnCalculation">
      <div class="form-group">
        <label for="round">{{ t('input.round') }}</label>
        <input
          type="number"
          value="1"
          v-model="formData.round_number"
          id="round"
          min="1"
          required
        />
      </div>
      <div class="datePicker ">
        <label for="date">{{ t('input.date') }}</label>
        <input
          type="date"
          v-model="selectedDate"
          id="date"
          required
        />
      </div>
      <div v-if="selectedRatingOption === '1to9'">
      <div class="form-group">
        <label for="courseRating">{{ t('input.courseRating_1to9') }}</label>

          {{ selectedCourse?.course_par_1_to_9 }}
        </div>
      </div>
      <div v-if="selectedRatingOption === '10to18'">
      <div class="form-group">
        <label for="courseRating">{{ t('input.courseRating_10to18') }}</label>

          {{ selectedCourse?.course_par_10_to_18 }}
        </div>
      </div>
      <div v-if="selectedRatingOption === 'all'">
      <div class="form-group" >
        <label for="courseRating">{{ t('input.courseRating_all') }}</label>
        {{ selectedCourse?.course_par_all }}
        </div>
      </div>

      <div class="form-group">
        <label for="slopeRating">{{ t('input.slopeRating') }}</label>
        {{ selectedCourse?.slope_rating }}
        <!--        <input type="number" v-model="formData.slope_rating" id="slopeRating" min="1" required/>-->
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
            <div class="holesHeadline">
              <label>{{ t('input.courseSelection') }}</label>
              <div class="radio-group">
                <label v-if="selectedCourse?.course_rating_1_to_9">
                  {{ t('input.courseSelection_1to9') }}
                  <input  type="radio" value="1to9" v-model="selectedRatingOption" />
                </label>
                <label v-if="selectedCourse?.course_rating_10_to_18">
                  {{ t('input.courseSelection_10to18') }}
                  <input  type="radio" value="10to18" v-model="selectedRatingOption" />
                </label>
                <label v-if="selectedCourse?.course_rating_all">
                  {{ t('input.courseSelection_all') }}
                  <input  type="radio" value="all" v-model="selectedRatingOption" />
                </label>
              </div>

            </div>

      <!-- Löcher -->
      <div class="holes-container">
        <div class="hole" v-for="(score, index) in length" :key="index">
          <label :for="'hole-' + (index)">{{ index + lengthStart}}{{ t('input.hole') }}</label>
          <input
            type="number"
            :id="'hole-' + (index + lengthStart -1)"
            v-model="formData.scores[index + lengthStart -1]"
            min="1"
            required
          />
        </div>
      </div>

      <!-- Absenden -->
      <button type="submit" class="submit-btn">{{ t('input.calculate') }}</button>
    </form>
  </div>
</template>

<style scoped>
@import '../style/calculation-input.css';
</style>
