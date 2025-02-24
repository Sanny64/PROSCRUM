<script setup lang="ts">
import { nextTick, onMounted, reactive, ref, watch } from "vue";
import GolfCourse from "@/components/golf-course.vue";
import AddGolfCourse from "@/components/add-golf-course.vue";
import type {Course, CourseWithoutID} from '../types/types.ts';
import { apiCallCourses } from "@/composables/api-call-courses.ts";
// import CourseFilter from "@/components/course-filter.vue";

const { apiResultCourse, getCoursesAPI, addCourseAPI, deleteCourseAPI } = apiCallCourses();
const courseList = apiResultCourse;
const filteredCourseList = ref<Course[]>([]);
const inputValue = ref<string>("");
const courseRatingValue = ref();
const slopeRatingValue = ref();

async function addCourse(newCourse: CourseWithoutID) {
  await addCourseAPI(newCourse);
  await nextTick();
  await getCoursesAPI();
}

async function deleteCourse(course: Course) {
  await deleteCourseAPI(course);
  await nextTick();
  await getCoursesAPI();
}

function filterCourses() {

  filteredCourseList.value = courseList.value.filter(course =>
    course.course_name.toLowerCase().includes(inputValue.value.toLowerCase())
  );

  /*Max Course Rating*/
  if (courseRatingValue.value) {
    filteredCourseList.value = filteredCourseList.value.filter(course =>
      course.course_rating_18 <= courseRatingValue.value
    );
  }

  /*Max Slope Rating*/
  if (slopeRatingValue.value) {
    filteredCourseList.value = filteredCourseList.value.filter(course =>
      course.slope_rating <= slopeRatingValue.value
    );
  }
}

watch([courseList, inputValue, courseRatingValue, slopeRatingValue], filterCourses);

onMounted(() => {
  getCoursesAPI();
});

function textValueFunc(textValue: string) {
  inputValue.value = textValue;
}

function courseRatingValueFunc(courseRatingValueFunc: number) {
  courseRatingValue.value = courseRatingValueFunc;
}

function slopeRatingValueFunc(slopeRatingValueFunc: number) {
  slopeRatingValue.value = slopeRatingValueFunc;
}

</script>

<template>
  <div class="content">
<!--    <div class="grid2">-->

<!--      <course-filter @text-value="textValueFunc" @course-rating-value="courseRatingValueFunc" @slope-rating-value="slopeRatingValueFunc" :course-list="courseList"></course-filter>-->
<!--    </div>-->
    <div class="grid">
      <div v-for="(course, index) in filteredCourseList" :key="course.course_id">
        <golf-course :course="course" @course-deleted="deleteCourse"></golf-course>
      </div>
      <add-golf-course @course-added="addCourse"></add-golf-course>
    </div>
  </div>
</template>

<style scoped>
@import "../style/CoursePage.css";
</style>
