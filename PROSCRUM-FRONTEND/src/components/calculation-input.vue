<script setup lang="ts">
import { ref, defineEmits, reactive, watchEffect } from 'vue'
import type { FormData, Course } from '../types/types.ts'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

let length = ref(18)
let isChecked = ref(true)

const props = defineProps<{
  courseList: Course[]
}>()

console.log('CourseList: ', props.courseList)

// Ausgewählte Option
const selectedCourseName = ref<string | null>('')
const selectedCourse = ref<Course>()

// Sichtbarkeit des Dropdown-Menüs steuern
const isDropdownOpen = ref(false)

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
  course: undefined,
  scores: [], // Initialisiertes Array
})

watchEffect(() => {
  formData.course = selectedCourse.value
})

// WatchEffect, um die Länge und Zufallswerte dynamisch zu setzen
watchEffect(() => {
  formData.scores = Array.from(
    { length: length.value },
    () => Math.floor(Math.random() * (10 - 1 + 1)) + 1, // Zufallszahlen zwischen 1 und 10
  )
})

function toggleCheckbox() {
  // Zustand explizit umschalten bei Enter-Taste
  isChecked.value = !isChecked.value
  handleCheckboxChange() // Aktualisiere den Zustand entsprechend
}

function handleCheckboxChange() {
  // Länge der Löcher basierend auf dem Zustand setzen
  if (isChecked.value) {
    length.value = 18
    console.log('Checkbox aktiviert. Länge: ' + length.value)
  } else {
    length.value = 9
    console.log('Checkbox deaktiviert. Länge: ' + length.value)
  }
}

const inputInfo = ref('')

const emit = defineEmits(['formData'])

const btnCalculation = () => {
  if (selectedCourseName.value === '') {
    console.log('Bitte wählen Sie einen Golfplatz')
  } else if (formData) {
    inputInfo.value = ''
    console.log('Emit gesendet: ', formData)
    emit('formData', formData)
  } else {
    console.log('Bitte geben Sie einen Wert ein')
    inputInfo.value = 'Bitte geben Sie einen Wert ein'
  }
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
      <div class="form-group" v-if="isChecked">
        <label for="courseRating">{{ t('input.courseRating') }}</label>
        {{ selectedCourse?.course_rating_18 }}
        <!--        <input type="number" step="0.1" v-model="formData.course_rating" id="courseRating" min="0.1" required/>-->
      </div>
      <div class="form-group" v-if="!isChecked">
        <label for="courseRating">{{ t('input.courseRating') }}</label>
        <!--        {{ selectedCourse?.course_rating_18 }}-->
        <input
          v-if="formData.course"
          type="number"
          step="0.1"
          id="courseRating"
          min="0.1"
          required
          v-model="formData.course.course_rating_9"
        />
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
        <h2>{{ t('input.holes') }}</h2>
        <p>9</p>
        <label class="switch" @keydown.enter.prevent="toggleCheckbox" tabindex="0">
          <input type="checkbox" v-model="isChecked" @change="handleCheckboxChange" tabindex="-1" />
          <span class="slider round"></span>
        </label>
        <p>18</p>
      </div>
      <!-- Löcher -->
      <div class="holes-container">
        <div class="hole" v-for="(score, index) in formData.scores" :key="index">
          <label :for="'hole-' + (index + 1)">{{ index + 1 }}{{ t('input.hole') }}</label>
          <input
            type="number"
            :id="'hole-' + (index + 1)"
            v-model="formData.scores[index]"
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
