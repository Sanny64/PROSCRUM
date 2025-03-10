<script setup lang="ts">
import type { Course } from '../types/types.ts'
import { computed, defineEmits, ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const emit = defineEmits(['course-deleted'])

const props = defineProps<{
  course: Course
}>()

let gridView = ref(true)

let iconNumber = ref()

/*course id mod 10 */
if (props.course.course_id) {
  iconNumber.value = (props.course.course_id % 10) + 1
}

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
  const path = new URL(`../assets/courseIcons`, import.meta.url)
  return `${path}/${iconNumber.value}.png`
})
</script>

<template>
  <div v-if="gridView" class="gridView" @click="openDetails()">
    <div class="gridViewText">
      <div class="gridViewHeadline">
        {{ props.course.course_name }}
        {{ props.course.course_id }}
      </div>
      <div class="gridViewDetails">
        <div>{{ t('coursePage.par') }}{{ props.course.course_par }}</div>
        <div>{{ t('coursePage.courseRating') }}{{ props.course.course_rating_18 }}</div>
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
      <div class="form-group">
        <label for="coursePar">{{ t('coursePage.par') }}</label>
        <b>{{ course.course_par }}</b>
      </div>
      <div class="form-group">
        <label for="courseRating">{{ t('coursePage.courseRating') }}</label>
        <b>{{ course.course_rating_18 }}</b>
      </div>
      <div class="form-group">
        <label for="slopeRating">{{ t('coursePage.slopeRating') }}</label>
        <b>{{ course.slope_rating }}</b>
      </div>

      <!-- Löcher -->
      <div class="holes-container">
        <div class="hole" v-for="hole in course.holes" :key="hole.hole">
          <label :for="'hole-' + hole.hole"
            >{{ hole.hole }}. {{ t('coursePage.hole') }}-> {{ t('coursePage.par') }}</label
          >
          <b>{{ hole.par }}</b>
          <label :for="'hole-' + hole.hole">{{ t('coursePage.hdc') }}</label>
          <b>{{ hole.hdc }}</b>
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
