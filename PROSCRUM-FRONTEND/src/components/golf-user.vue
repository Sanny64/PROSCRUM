<script setup lang="ts">
import type {Course, Round, User} from '../types/types.ts'
import {computed, defineEmits, onMounted, ref, watchEffect} from 'vue'
import { useI18n } from 'vue-i18n'
import Info from "@/components/info.vue";
import { apiCallRounds } from '@/composables/api-call-rounds.ts'
const {} = apiCallRounds()


const { t } = useI18n()
const emit = defineEmits(['updated-round'])
const editMode = ref(false);

const props = defineProps<{
  user: User
}>()

let gridView = ref(true)
const selectedRatingOption = ref<'all' | '1to9' | '10to18'>('all')
let length = ref(18)
let lengthStart = ref(0)
let iconNumber = ref()




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
  emit('updated-round', props.user)
}


</script>

<template>
  <div v-if="gridView" class="gridView" @click="openDetails()">
    <div class="gridViewText">
      <div class="gridViewHeadline">{{t('usersPage.full_name')}}{{ props.user.first_name}} {{ props.user.last_name}}</div>
      <div class="gridViewDetails">
        <div>{{t('usersPage.role_id')}}{{ props.user.role_id}}</div>
      </div>
    </div>
  </div>

  <div class="inputView" v-if="!gridView && !editMode">
    <div class="formView">
              <div class="form-group number">
                <label for="round">{{t('usersPage.email')}}</label>
                <b>{{props.user.email}}</b>
              </div>
              <div class="form-group date">
                <label for="round">{{t('usersPage.created_at')}}</label>
                <b>{{props.user.created_at.split('T')[0]}}</b>
              </div>


      <button class="submit-btn" @click="closeDetails()">{{ t('roundPage.close') }}</button>
    </div>
  </div>

<!--  Update Mode-->

</template>

<style scoped>
@import '../style/golf-round.css';
</style>
