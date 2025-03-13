<script setup lang="ts">
import type { Course } from '../types/types.ts'
import {computed, defineEmits, ref, watchEffect} from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const emit = defineEmits(['course-deleted'])

const props = defineProps<{
  course: Course
}>()

let gridView = ref(true)
const selectedRatingOption = ref<'all' | '1to9' | '10to18'>('all')
let length = ref(18)
let lengthStart = ref(0)
let iconNumber = ref()

/*course id mod 10 */
if (props.course.course_id) {
  iconNumber.value = (props.course.course_id % 10) + 1
}

watchEffect(() => {
  // Länge der Löcher basierend auf dem Zustand setzen
  if (selectedRatingOption.value === '1to9' ) {
    length.value = 9
    lengthStart.value = 1
  }else if(selectedRatingOption.value === '10to18'){
    length.value = 9
    lengthStart.value = 10
  }else {
    lengthStart.value = 1
    length.value = 18
  }
});

function closeDetails() {
  gridView.value = true
}

function openDetails() {
  gridView.value = false
}

function deleteCourse() {
  gridView.value = true
  console.log('Send Emit')
  emit('course-deleted', props.course)
}


const src = computed(() => {
  return `/courseIcons/${iconNumber.value}.png`
})

</script>

<template>
  <div v-if="gridView" class="gridView" @click="openDetails()">
    <div class="gridViewText">
      <div class="gridViewHeadline">
        {{ props.course.course_name }}
      </div>
      <div class="gridViewDetails">
        <div>{{ t('coursePage.par') }}{{ props.course.course_par_all }}</div>
        <div>{{ t('coursePage.courseRating') }}{{ props.course.course_rating_all }}</div>
        <div>{{ t('coursePage.slopeRating') }}{{ props.course.slope_rating }}</div>
      </div>
    </div>
    <div class="gridViewImage">
      <img :src="src" />
    </div>
  </div>

  <div class="inputView" v-if="!gridView">
    <div class="formView">
      <div class="form-group">
        <label for="round">{{ t('coursePage.courseName') }}</label>
        <b>{{ course.course_name }}</b>
      </div>
      <div v-if="selectedRatingOption === '1to9'">
        <div class="form-group">
          <label for="courseRating">{{t('coursePage.courseRating_1to9')}}</label>

          <b>{{ props.course?.course_rating_1_to_9 }}</b>
        </div>
      </div>
      <div v-if="selectedRatingOption === '10to18'">
        <div class="form-group">
          <label for="courseRating">{{ t('coursePage.courseRating_10to18') }}</label>

          <b>{{ props.course?.course_rating_10_to_18 }}</b>
        </div>
      </div>
      <div v-if="selectedRatingOption === 'all'">
        <div class="form-group" >
          <label for="courseRating">{{ t('coursePage.courseRating_all') }}</label>
          <b>{{ props.course?.course_rating_all}}</b>
        </div>
      </div>
      <div v-if="selectedRatingOption === '1to9'">
        <div class="form-group">
          <label for="courseRating">{{ t('coursePage.course_par_1to9') }}</label>

          <b>{{props.course?.course_par_1_to_9 }}</b>
        </div>
      </div>
      <div v-if="selectedRatingOption === '10to18'">
        <div class="form-group">
          <label for="courseRating">{{ t('coursePage.course_par_10to18') }}</label>

          <b>{{ props.course?.course_par_10_to_18 }}</b>
        </div>
      </div>
      <div v-if="selectedRatingOption === 'all'">
        <div class="form-group" >
          <label for="courseRating">{{ t('coursePage.course_par_all') }}</label>
          <b>{{ props.course?.course_par_all }}</b>
        </div>
      </div>

      <div class="form-group">
        <label for="slopeRating">{{ t('coursePage.slopeRating') }}</label>
        <b>{{ props.course?.slope_rating }}</b>
        <!--        <input type="number" v-model="formData.slope_rating" id="slopeRating" min="1" required/>-->
      </div>

      <!-- Switch -->
      <div class="holesHeadline">
        <label>{{ t('coursePage.courseSelection') }}</label>
        <div class="radio-group">
          <label v-if="props.course?.course_rating_1_to_9" class="radio-button">
            {{ t('coursePage.courseSelection_1to9') }}
            <input  type="radio" value="1to9" v-model="selectedRatingOption" />
          </label>
          <label v-if="props.course?.course_rating_10_to_18" class="radio-button">
            {{ t('coursePage.courseSelection_10to18') }}
            <input  type="radio" value="10to18" v-model="selectedRatingOption" />
          </label>
          <label v-if="props.course?.course_rating_all" class="radio-button">
            {{ t('coursePage.courseSelection_all') }}
            <input  type="radio" value="all" v-model="selectedRatingOption" />
          </label>
        </div>

      </div>

      <!-- Löcher -->
      <div class="holes-container">
        <div class="hole" v-for="(score, index) in length" :key="index">
          <b :for="'hole-' + (index)">{{ index + lengthStart}} {{ t('coursePage.hole') }}</b>
          <label>{{ t('coursePage.par') }}</label>
          <b>{{props.course?.holes[index + lengthStart -1].par }}</b>
          <label >{{ t('coursePage.hdc') }}</label>
          <b>{{ props.course?.holes[index + lengthStart -1].hdc }}</b>
        </div>
      </div>
      <button class="submit-btn" @click="deleteCourse()">{{ t('coursePage.delete') }}</button>
      <button class="submit-btn" @click="closeDetails()">{{ t('coursePage.close') }}</button>
    </div>
  </div>
</template>

<style scoped>
@import '../style/golf-course.css';
</style>
