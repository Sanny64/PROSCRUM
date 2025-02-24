<script setup lang="ts">
import {computed, type ComputedRef, defineEmits, reactive, ref, watchEffect} from "vue";
import type {CourseWithoutID} from '../types/types.ts';
import Info from "@/components/info.vue";

import { useI18n } from 'vue-i18n';

import { watch } from "vue";

const info = ref<boolean>(false);
const infoText = ref<string>("");
const {t} = useI18n();
const emit = defineEmits(['course-added']);

let gridView = ref<boolean>(true);

const sumPar: ComputedRef<number> = computed(() => {
  return newCourse.holes.reduce((sum, hole) => {
    return sum + (hole.par || 0);
  }, 0);
});

const newCourse = reactive<CourseWithoutID>(
  {
    course_name: "Platz 3 - Windige Wiese",
    course_par: 0,
    course_rating_9: null,
    course_rating_18: 74,
    slope_rating: 128,
    holes: [
      {hole: 1, par: 4, hdc: 12},
      {hole: 2, par: 3, hdc: 18},
      {hole: 3, par: 5, hdc: 6},
      {hole: 4, par: 4, hdc: 14},
      {hole: 5, par: 4, hdc: 2},
      {hole: 6, par: 3, hdc: 16},
      {hole: 7, par: 5, hdc: 8},
      {hole: 8, par: 4, hdc: 4},
      {hole: 9, par: 4, hdc: 10},
      {hole: 10, par: 4, hdc: 11},
      {hole: 11, par: 3, hdc: 17},
      {hole: 12, par: 5, hdc: 7},
      {hole: 13, par: 4, hdc: 3},
      {hole: 14, par: 4, hdc: 1},
      {hole: 15, par: 3, hdc: 15},
      {hole: 16, par: 5, hdc: 9},
      {hole: 17, par: 4, hdc: 5},
      {hole: 18, par: 4, hdc: 13}
    ]
  }
);

watchEffect(() => {
  newCourse.course_par = sumPar.value;
});

function handleAddCourse() {
  if (validateHDC()) {
    info.value = true;
    return;
  }
  gridView.value = true;
  emit('course-added', newCourse);
}

function closeForm() {
  gridView.value = true;
}

function createCourse() {
  gridView.value = false;
}
const list = reactive({
  Hols: Array.from({ length: 18 }, (_, i) => i + 1),
  Belegt: Array(18).fill(false)
});

function validateHDC() {
  let hdcValues = newCourse.holes.map(hole => hole.hdc);
  let seen = new Set();

  for (let hdc of hdcValues) {
    if (typeof hdc !== "number" || hdc < 1 || hdc > 18) {

      infoText.value = `Error: HDC ${hdc} is outside the range 1-18. (i18n)`;
      return true;
    }

    if (seen.has(hdc)) {
      infoText.value = `Error: HDC ${hdc} is assigned twice.(i18n)`;
      return true;
    }

    seen.add(hdc);
  }

  console.log("✅ HDC-Werte sind gültig.");
  return false;
}


watch(
  () => newCourse.holes.map(hole => hole.hdc),
  () => {
    info.value = validateHDC();
  },
  { deep: true } // Erfasst Änderungen in den Objekten
);

function closeFunc(){
  info.value = false;
}


</script>

<template>

  <div v-if="gridView" class="gridView" @click="createCourse()">
    <svg  xmlns="http://www.w3.org/2000/svg"  width="48"  height="48"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-library-plus"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M7 3m0 2.667a2.667 2.667 0 0 1 2.667 -2.667h8.666a2.667 2.667 0 0 1 2.667 2.667v8.666a2.667 2.667 0 0 1 -2.667 2.667h-8.666a2.667 2.667 0 0 1 -2.667 -2.667z" /><path d="M4.012 7.26a2.005 2.005 0 0 0 -1.012 1.737v10c0 1.1 .9 2 2 2h10c.75 0 1.158 -.385 1.5 -1" /><path d="M11 10h6" /><path d="M14 7v6" /></svg>
  </div>
  <div class="inputView" v-if="!gridView">
    <div class="formView">

      <form @submit.prevent="handleAddCourse()">
        <div class="form-group">
          <label for="round">{{t('coursePage.courseName')}}</label>
          <input type="Text" value="1" v-model="newCourse.course_name" id="course_name" min="1" required/>
        </div>
        <div class="form-group">
          <label for="courseRating">{{t('coursePage.courseRating')}}</label>
          <input type="number" step="0.1" v-model="newCourse.course_rating_18" id="courseRating" min="0.1" required/>
        </div>
        <div class="form-group">
          <label for="slopeRating">{{t('coursePage.slopeRating')}}</label>
          <input type="number" v-model="newCourse.slope_rating" id="slopeRating" min="1" required/>
        </div>
        <div class="form-group">
          <label for="courseRating">{{t('coursePage.par')}}</label>
          <b>{{newCourse.course_par}}</b>
        </div>

        <!-- Löcher -->
        <div class="holes-container">
          <div
            class="hole"
            v-for="(hole) in newCourse.holes"
            :key="hole.hole"
          >
            <label :for="'hole-' + hole.hole">{{ hole.hole }}. {{t('coursePage.hole')}}-> {{t('coursePage.par')}}</label>
            <input
              type="number"
              :id="'hole-' + hole.hole"
              v-model="hole.par"
              min="1"
              required
            />
            <label :for="'hole-' + hole.hole">{{t('coursePage.hdc')}}</label>
            <input
              type="number"
              :id="'hole-' + hole.hole"
              v-model="hole.hdc"
              min="1"
              required
            />
          </div>

        </div>

        <!-- Absenden -->
        <button type="submit" class="submit-btn">{{t('coursePage.save')}}</button>
        <button type="button" class="submit-btn" @click="closeForm()">{{t('coursePage.close')}}</button>
      </form>

      <info v-if="info" @close="closeFunc" :infoText="infoText"></info>
    </div>
  </div>

</template>

<style scoped>
@import "../style/add-golf-course.css";
</style>
