<script setup lang="ts">
import type {Course, Round} from '../types/types.ts'
import {computed, defineEmits, onMounted, ref, watchEffect} from 'vue'
import { useI18n } from 'vue-i18n'
import Info from "@/components/info.vue";

const { t } = useI18n()
const emit = defineEmits(['updated-round'])
const editMode = ref(false);

const props = defineProps<{
  rounds: Round
}>()

let gridView = ref(true)
const selectedRatingOption = ref<'all' | '1to9' | '10to18'>('all')
let length = ref(18)
let lengthStart = ref(0)
let iconNumber = ref()



onMounted(() => {
  determineSelectedRatingOption(props.rounds)
})

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



 function determineSelectedRatingOption(round: Round) {
  const scores = round.scores

  const firstNineZeros = scores.slice(0, 9).every(score => score === 0)
  const lastNineZeros = scores.slice(-9).every(score => score === 0)

  if (firstNineZeros && lastNineZeros) {
    selectedRatingOption.value = 'all'
  } else if (firstNineZeros) {
    selectedRatingOption.value = '10to18'
  } else if (lastNineZeros) {
    selectedRatingOption.value = '1to9'
  } else {
    selectedRatingOption.value = 'all'
  }
}



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
      <div class="gridViewHeadline">{{t('roundMasterPage.player_name')}}{{ props.rounds.user.first_name }} {{ props.rounds.user.last_name }}</div>
      <div class="gridViewDetails">
        <div>{{t('roundMasterPage.round_number')}}{{ props.rounds.round_number }}</div>
      </div>

    </div>
  </div>

  <div class="inputView" v-if="!gridView && !editMode">
    <div class="formView">

                <div class="form-group player">
                <label for="round">{{t('roundMasterPage.player_name')}}</label>
                <b>{{ props.rounds.user.first_name }} {{ props.rounds.user.last_name }}</b>
              </div>
      <div class="form-group number">
        <label for="round">{{t('roundMasterPage.round_number')}}</label>
        <b>{{props.rounds.round_number}}</b>
      </div>
              <div class="form-group date">
                <label for="round">{{t('roundMasterPage.date')}}</label>
                <b>{{props.rounds.date}}</b>
              </div>
              <div class="form-group">
                <label for="round">{{t('roundMasterPage.courseName')}}</label>
                <b>{{props.rounds.course.course_name}}</b>
              </div>

      <div v-if="selectedRatingOption === '1to9'">
        <div class="form-group">
          <label for="courseRating">{{ t('roundMasterPage.courseRating_1to9') }}</label>

          <b>{{ props.rounds.course?.course_rating_1_to_9 }}</b>
        </div>
      </div>
      <div v-if="selectedRatingOption === '10to18'">
        <div class="form-group">
          <label for="courseRating">{{ t('roundMasterPage.courseRating_10to18') }}</label>

          <b>{{  props.rounds.course?.course_rating_10_to_18 }}</b>
        </div>
      </div>
      <div v-if="selectedRatingOption === 'all'">
        <div class="form-group" >
          <label for="courseRating">{{ t('roundMasterPage.courseRating_all') }}</label>
          <b>{{  props.rounds.course?.course_rating_all }}</b>
        </div>
      </div>
      <div v-if="selectedRatingOption === '1to9'">
        <div class="form-group">
          <label for="courseRating">{{ t('roundMasterPage.course_par_1to9') }}</label>

          <b>{{ props.rounds.course?.course_par_1_to_9 }}</b>
        </div>
      </div>
      <div v-if="selectedRatingOption === '10to18'">
        <div class="form-group">
          <label for="courseRating">{{ t('roundMasterPage.course_par_10to18') }}</label>

          <b>{{  props.rounds.course?.course_par_10_to_18 }}</b>
        </div>
      </div>
      <div v-if="selectedRatingOption === 'all'">
        <div class="form-group" >
          <label for="courseRating">{{ t('roundMasterPage.course_par_all') }}</label>
          <b>{{  props.rounds.course?.course_par_all }}</b>
        </div>
      </div>

              <div class="form-group">
                <label for="slopeRating">{{t('roundMasterPage.slopeRating')}}</label>
                <b>{{props.rounds.course.slope_rating}}</b>
              </div>

              <!-- Löcher -->
                <div class="holes-container">
                  <div class="hole" v-for="(score, index) in length" :key="index">
                    <b :for="'hole-' + (index)">{{ index + lengthStart}}. {{ t('coursePage.hole') }}</b>
                    <label>{{ t('roundPage.shots') }}</label>
                    <b>{{props.rounds.scores[index + lengthStart -1]}}</b>
                    <label>{{ t('coursePage.par') }}</label>
                    <b>{{props.rounds.course?.holes[index + lengthStart -1].par }}</b>
                    <label >{{ t('coursePage.hdc') }}</label>
                    <b>{{ props.rounds.course?.holes[index + lengthStart -1].hdc }}</b>
                  </div>
                </div>


      <button class="submit-btn" @click="openUpdate()" >{{t('roundMasterPage.update')}}</button>
      <button class="submit-btn" @click="closeDetails()">{{ t('roundMasterPage.close') }}</button>
    </div>
  </div>

<!--  Update Mode-->

  <div class="inputView" v-if="!gridView && editMode">
    <div class="formView">
      <form @submit.prevent="updateRound()">
        <div class="form-group date">
          <label for="round">{{t('roundMasterPage.date')}}</label>
          <b>{{props.rounds.date}}</b>
        </div>
        <div class="form-group number">
          <label for="round">{{t('roundMasterPage.round_number')}}</label>
          <b>{{props.rounds.round_number}}</b>
        </div>
        <div class="form-group">
          <label for="round">{{t('roundMasterPage.courseName')}}</label>
          <b>{{props.rounds.course.course_name}}</b>
        </div>

        <div v-if="selectedRatingOption === '1to9'">
          <div class="form-group">
            <label for="courseRating">{{ t('roundMasterPage.courseRating_1to9') }}</label>

            <b>{{ props.rounds.course?.course_rating_1_to_9 }}</b>
          </div>
        </div>
        <div v-if="selectedRatingOption === '10to18'">
          <div class="form-group">
            <label for="courseRating">{{ t('roundMasterPage.courseRating_10to18') }}</label>

            <b>{{  props.rounds.course?.course_rating_10_to_18 }}</b>
          </div>
        </div>
        <div v-if="selectedRatingOption === 'all'">
          <div class="form-group" >
            <label for="courseRating">{{ t('roundMasterPage.courseRating_all') }}</label>
            <b>{{  props.rounds.course?.course_rating_1_to_9 }}</b>
          </div>
        </div>
        <div v-if="selectedRatingOption === '1to9'">
          <div class="form-group">
            <label for="courseRating">{{ t('roundMasterPage.course_par_1to9') }}</label>

            <b>{{ props.rounds.course?.course_par_1_to_9 }}</b>
          </div>
        </div>
        <div v-if="selectedRatingOption === '10to18'">
          <div class="form-group">
            <label for="courseRating">{{ t('roundMasterPage.course_par_10to18') }}</label>

            <b>{{  props.rounds.course?.course_par_10_to_18 }}</b>
          </div>
        </div>
        <div v-if="selectedRatingOption === 'all'">
          <div class="form-group" >
            <label for="courseRating">{{ t('roundMasterPage.course_par_all') }}</label>
            <b>{{  props.rounds.course?.course_par_all }}</b>
          </div>
        </div>

        <div class="form-group">
          <label for="slopeRating">{{t('roundMasterPage.slopeRating')}}</label>
          <b>{{props.rounds.course.slope_rating}}</b>
        </div>

        <!-- Löcher -->
        <div class="holes-container">
          <div class="hole" v-for="(score, index) in length" :key="index">
            <b :for="'hole-' + (index)">{{ index + lengthStart}}. {{ t('coursePage.hole') }}</b>
            <label>{{ t('roundPage.shots') }}</label>
            <input
              type="number"
              v-model="props.rounds.scores[index + lengthStart -1]"
              min="1"
              required>
            <label>{{ t('coursePage.par') }}</label>
            <b>{{props.rounds.course?.holes[index + lengthStart -1].par }}</b>
            <label >{{ t('coursePage.hdc') }}</label>
            <b>{{ props.rounds.course?.holes[index + lengthStart -1].hdc }}</b>
          </div>
        </div>




        <!-- Absenden -->
        <button type="submit" class="submit-btn">{{ t('roundMasterPage.update') }}</button>
        <button type="button" class="submit-btn" @click="backDetails()">
          {{ t('roundPage.back') }}
        </button>
      </form>

<!--      <info v-if="info" @close="closeFunc" :infoText="infoText"></info>-->
    </div>
  </div>
</template>

<style scoped>
@import '../style/golf-user-round.css';
</style>
