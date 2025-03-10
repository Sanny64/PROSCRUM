<script setup lang="ts">
import CalculationOutput from '../components/calculation-output.vue'
import CalculationInput from '../components/calculation-input.vue'
import type { FormData } from '../types/types.ts'
import { apiCallInlineResponse } from '@/composables/api-call-inline-response.ts'
import { apiCallCourses } from '@/composables/api-call-courses.ts'
import { apiCallRounds } from '@/composables/api-call-rounds.ts'
import { onMounted, watch, watchEffect } from 'vue'

const { apiResultRounds, getRoundsAPI } = apiCallRounds()
const { apiResultCourse, getCoursesAPI } = apiCallCourses()
const { apiStatus, sendFormdata } = apiCallInlineResponse()
const handleFormData = (formdata: FormData) => {
  sendFormdata(formdata)
}

onMounted(() => {
  getCoursesAPI()
  getRoundsAPI()
})

watch(apiStatus, (newValue) => {
  console.log('apiStatus changed:', newValue)
  if (newValue === 201) {
    getRoundsAPI()
  }
})
</script>

<template>
  <div class="content">
    <calculation-input
      @formData="handleFormData"
      :course-list="apiResultCourse"
    ></calculation-input>
    <calculation-output
      :polling-status="apiStatus"
      :rounds-result="apiResultRounds"
    ></calculation-output>
  </div>
</template>

<style scoped>
@import '../style/HomePage.css';
</style>
