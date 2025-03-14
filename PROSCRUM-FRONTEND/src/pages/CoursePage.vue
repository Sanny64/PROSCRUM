<script setup lang="ts">
import {inject, nextTick, onMounted, reactive, type Ref, ref, watch} from 'vue'
import GolfCourse from '@/components/golf-course.vue'
import AddGolfCourse from '@/components/add-golf-course.vue'
import type {Course, CourseWithoutID, User} from '../types/types.ts'
import { apiCallCourses } from '@/composables/api-call-courses.ts'
import CourseFilter from '@/components/course-filter.vue'
import {apiCallUser} from "@/composables/api-call-user.ts";

const { apiResultCourse, getCoursesAPI, addCourseAPI, deleteCourseAPI } = apiCallCourses()
const courseList = apiResultCourse
const {getUserAllAPI, allUserList} = apiCallUser()

const userList = allUserList

const filteredCourseList = ref<Course[]>([])
const inputValue = ref<string>('')
const courseRatingValue = ref()
const slopeRatingValue = ref()
const activeUserAPI = inject<Ref<User | 'INVALID'>>("activeUser", ref("INVALID"));


async function addCourse(newCourse: CourseWithoutID) {
  await addCourseAPI(newCourse)
  await nextTick()
  await getCoursesAPI()
}

async function deleteCourse(course: Course) {
  await deleteCourseAPI(course)
  await nextTick()
  await getCoursesAPI()
}

function filterCourses() {
  filteredCourseList.value = courseList.value.filter((course) =>
    course.course_name.toLowerCase().includes(inputValue.value.toLowerCase()),
  )

  /*Max Course Rating*/
  if (courseRatingValue.value){
    filteredCourseList.value = filteredCourseList.value.filter(
      (course) => course.course_rating_all <= courseRatingValue.value,
    )
  }

  /*Max Slope Rating*/
  if (slopeRatingValue.value) {
    filteredCourseList.value = filteredCourseList.value.filter(
      (course) => course.slope_rating <= slopeRatingValue.value,
    )
  }
}

watch([courseList, inputValue, courseRatingValue, slopeRatingValue], filterCourses)

onMounted(() => {
  getCoursesAPI()
  if(activeUserAPI.value != 'INVALID' && activeUserAPI.value.role_id > 2) {
    getUserAllAPI()
  }
})

function textValueFunc(textValue: string) {
  inputValue.value = textValue
}

function courseRatingValueFunc(courseRatingValueFunc: number) {
  courseRatingValue.value = courseRatingValueFunc
}

function slopeRatingValueFunc(slopeRatingValueFunc: number) {
  slopeRatingValue.value = slopeRatingValueFunc
}
</script>

<template>
  <div class="content">
    <div class="filterGrid">
      <course-filter
        @text-value="textValueFunc"
        @course-rating-value="courseRatingValueFunc"
        @slope-rating-value="slopeRatingValueFunc"
        :course-list="courseList"
      ></course-filter>
    </div>
    <div class="grid">
      <div v-for="(course, index) in filteredCourseList" :key="course.course_id">
        <golf-course :course="course" @course-deleted="deleteCourse"></golf-course>
      </div>
      <add-golf-course v-if="activeUserAPI !='INVALID' && activeUserAPI.role_id > 2" @course-added="addCourse" :user-list="userList"></add-golf-course>
    </div>
  </div>
</template>

<style scoped>
@import '../style/CoursePage.css';
</style>
