<script setup lang="ts">
import type { Course } from '../types/types.ts'
import { computed, defineEmits, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import Info from "@/components/info.vue";

const { t } = useI18n()
const emit = defineEmits(['updated-round'])
const editMode = ref(false);

const props = defineProps<{
  rounds: any
}>()

let gridView = ref(true)

let iconNumber = ref()

/*course id mod 10 */

function closeDetails() {
  gridView.value = true
}

function openDetails() {
  gridView.value = false
}

function openUpdate() {
  editMode.value = true;
}

function backDetails() {
  gridView.value = false
  editMode.value = false;
}

function updateRound() {
  editMode.value = false;
  gridView.value = true;
  emit('updated-round', props.rounds)
}


</script>

<template>
  <div v-if="gridView" class="gridView" @click="openDetails()">
    <div class="gridViewText">
      <div class="gridViewHeadline">{{t('roundPage.round_number')}}{{ props.rounds.round_number }}</div>
      <div class="gridViewDetails">
        <div>{{t('roundPage.courseName')}}{{ props.rounds.course.course_name }}</div>
      </div>
    </div>
  </div>

  <div class="inputView" v-if="!gridView && !editMode">
    <div class="formView">
              <div class="form-group number">
                <label for="round">{{t('roundPage.round_number')}}</label>
                <b>{{props.rounds.round_number}}</b>
              </div>
              <div class="form-group date">
                <label for="round">{{t('roundPage.date')}}</label>
                <b>{{props.rounds.date}}</b>
              </div>
              <div class="form-group">
                <label for="round">{{t('roundPage.courseName')}}</label>
                <b>{{props.rounds.course.course_name}}</b>
              </div>
              <div class="form-group">
                <label for="coursePar">{{t('roundPage.par')}}</label>
                <b>{{props.rounds.course.course_par}}</b>
              </div>
              <div class="form-group">
                <label for="courseRating">{{t('roundPage.courseRating')}}</label>
                <b>{{props.rounds.course.course_rating_18}}</b>
              </div>
              <div class="form-group">
                <label for="slopeRating">{{t('roundPage.slopeRating')}}</label>
                <b>{{props.rounds.course.slope_rating}}</b>
              </div>

              <!-- Löcher -->
              <div class="holes-container">
                <div
                  class="hole"
                  v-for="(hole) in props.rounds.course.holes"
                  :key="hole.hole"
                >
                  <b :for="'hole-' + hole.hole">{{ hole.hole }}. {{t('coursePage.hole')}}</b>
                    <label>{{t('roundPage.score')}}</label>
                  <b>{{props.rounds.scores[hole.hole - 1]}}</b>
                  <label :for="'hole-' + hole.hole">{{t('coursePage.par')}}</label>
                  <b>{{hole.par}}</b>
                  <label :for="'hole-' + hole.hole">{{t('roundPage.hdc')}}</label>
                  <b>{{hole.hdc}}</b>

                </div>

              </div>
      <button class="submit-btn" @click="openUpdate()" >{{t('roundPage.update')}}</button>
      <button class="submit-btn" @click="closeDetails()">{{ t('roundPage.close') }}</button>
    </div>
  </div>

<!--  Update Mode-->

  <div class="inputView" v-if="!gridView && editMode">
    <div class="formView">
      <form @submit.prevent="updateRound()">
        <div class="form-group">
          <label for="round">{{t('roundPage.round_number')}}</label>
          <b>{{props.rounds.round_number}}</b>
        </div>
        <div class="form-group">
          <label for="round">{{t('roundPage.courseName')}}</label>
          <b>{{props.rounds.course.course_name}}</b>
        </div>
        <div class="form-group">
          <label for="coursePar">{{t('roundPage.par')}}</label>
          <b>{{props.rounds.course.course_par}}</b>
        </div>
        <div class="form-group">
          <label for="courseRating">{{t('roundPage.courseRating')}}</label>
          <b>{{props.rounds.course.course_rating_18}}</b>
        </div>
        <div class="form-group">
          <label for="slopeRating">{{t('roundPage.slopeRating')}}</label>
          <b>{{props.rounds.course.slope_rating}}</b>
        </div>

        <!-- Löcher -->
        <div class="holes-container">
          <div
            class="hole"
            v-for="(hole) in props.rounds.course.holes"
            :key="hole.hole"
          >
            <b :for="'hole-' + hole.hole">{{ hole.hole }}. {{t('coursePage.hole')}}</b>
            <label>{{t('roundPage.score')}}</label>
            <input
              type="number"
              :id="'hole-' + hole.hole"
              v-model="props.rounds.scores[hole.hole - 1]"
              min="1"
              required>
            <label :for="'hole-' + hole.hole">{{t('coursePage.par')}}</label>
            <b>{{hole.par}}</b>
            <label :for="'hole-' + hole.hole">{{t('roundPage.hdc')}}</label>
            <b>{{hole.hdc}}</b>

          </div>

        </div>

        <!-- Absenden -->
        <button type="submit" class="submit-btn">{{ t('roundPage.update') }}</button>
        <button type="button" class="submit-btn" @click="backDetails()">
          {{ t('roundPage.back') }}
        </button>
      </form>

<!--      <info v-if="info" @close="closeFunc" :infoText="infoText"></info>-->
    </div>
  </div>
</template>

<style scoped>
@import '../style/golf-round.css';
</style>
