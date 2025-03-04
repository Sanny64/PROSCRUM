<script setup lang="ts">
import { ref, watch, defineEmits, onMounted, computed } from 'vue'
import type {Course, Round} from '@/types/types.ts'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const emit = defineEmits()

const props = defineProps<{
  roundsList: Round[]
}>()

const textValue = ref<string>('')
const numberValue = ref<number>()
const courseRatingValue = ref<number>()
const slopeRatingValue = ref<number>()

const CourseList = ref<Course[]>([])

let disableMaxSlopeRatingBoolean = ref<boolean>()
let disableMaxCourseRatingBoolean = ref<boolean>(false)
let tempMaxSlopeRatingValue: number | undefined
let tempMaxCourseRatingValue: number | undefined

const highestCourseRatingValue = ref()
const highestSlopeRatingValue = ref()
let loadFilter = ref(false)

watch(textValue, (newValue) => {
  emit('text-value', newValue)
})

watch(numberValue, (newValue) => {
  emit('number-value', newValue)
})

watch(courseRatingValue, (newValue) => {
  emit('course-rating-value', newValue)
})

watch(slopeRatingValue, (newValue) => {
  emit('slope-rating-value', newValue)
})

function disableMaxSlopeRating() {
  if (disableMaxSlopeRatingBoolean.value) {
    disableMaxSlopeRatingBoolean.value = !disableMaxSlopeRatingBoolean.value
    slopeRatingValue.value = tempMaxSlopeRatingValue
  } else {
    disableMaxSlopeRatingBoolean.value = !disableMaxSlopeRatingBoolean.value
    tempMaxSlopeRatingValue = slopeRatingValue.value
    slopeRatingValue.value = undefined
  }
}

function disableMaxCourseRating() {
  if (disableMaxCourseRatingBoolean.value) {
    disableMaxCourseRatingBoolean.value = !disableMaxCourseRatingBoolean.value
    courseRatingValue.value = tempMaxCourseRatingValue
  } else {
    disableMaxCourseRatingBoolean.value = !disableMaxCourseRatingBoolean.value
    tempMaxCourseRatingValue = courseRatingValue.value
    courseRatingValue.value = undefined
  }
}

const highestSlopeRating = computed(() => {
  return 100
})

// Berechnet den höchsten Course Rating Wert
const highestCourseRating = computed(() => {
  return 100
})

watch(
  () => props.roundsList,
  (newValue, oldValue) => {
    console.log('highestSlopeRating: ', highestSlopeRating.value)
    console.log('highestCourseRating: ', highestCourseRating.value)
    highestSlopeRatingValue.value = highestSlopeRating.value
    highestCourseRatingValue.value = highestCourseRating.value
    loadFilter.value = true
  },
  { deep: true },
)
</script>

<template>
  <div v-if="loadFilter" class="filter2">
    <div class="TextInputContainer">
      <input
        :placeholder="$t('filter.search')"
        v-model="textValue"
        id="input"
        class="input"
        name="text"
        type="text"
      />
      <label class="labelforsearch" for="input">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="icon icon-tabler icons-tabler-outline icon-tabler-search"
        >
          <path stroke="none" d="M0 0h24v24H0z" fill="none" />
          <path d="M10 10m-7 0a7 7 0 1 0 14 0a7 7 0 1 0 -14 0" />
          <path d="M21 21l-6 -6" />
        </svg>
      </label>
    </div>

    <div class="NumberInputContainer">
      <input
        placeholder="Zahl(i18n)"
        v-model="numberValue"
        id="input"
        class="input"
        name="text"
        type="number"
      />
    </div>
  </div>
</template>

<style scoped>
@import '../style/rounds-filter.css';
</style>
