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
  roundsList: Round[]
}>()

let gridView = ref(true)


const latestRound = computed(() =>
  props.roundsList
    .filter((round: Round) => round.user.user_id === props.user.user_id)
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())[0] || null // Falls keine Runde existiert, `null`
);

const userRole = computed(() => {
  if (props.user.role_id === 1) {
    return t('usersPage.player')
  } else if (props.user.role_id === 2) {
    return t('usersPage.round_master')
  }  else if (props.user.role_id === 3) {
    return t('usersPage.secretary')
  } else {
    return t('usersPage.admin')
  }
})

function closeDetails() {
  gridView.value = true
}

function openDetails() {
  gridView.value = false
}

</script>

<template>
  <div v-if="gridView" class="gridView" @click="openDetails()">
    <div class="gridViewText">
      <div class="gridViewHeadline">{{t('usersPage.user_id')}}{{ props.user.user_id}} - {{ props.user.first_name}} {{ props.user.last_name}}</div>
      <div class="gridViewDetails">
        <div>{{t('usersPage.role_id')}}{{userRole}}</div>
      </div>
    </div>
  </div>

  <div class="inputView" v-if="!gridView && !editMode">
    <div class="formView">
              <div class="form-group">
                <label for="round">{{t('usersPage.email')}}</label>
                <b>{{props.user.email}}</b>
              </div>
              <div class="form-group">
                <label for="round">{{t('usersPage.created_at')}}</label>
                <b>{{props.user.created_at.split('T')[0]}}</b>
              </div>
            <div v-if="latestRound" >
              <div class="form-group">
              <label for="round">{{t('usersPage.hdc_2020')}}</label>
              <b>{{latestRound.calc_result_2020}}</b>
              </div>
              <div class="form-group">
              <label for="round">{{t('usersPage.hdc_2021')}}</label>
              <b>{{latestRound.calc_result_2021}}</b>
              </div>
            </div>


      <button class="submit-btn" @click="closeDetails()">{{ t('roundPage.close') }}</button>
    </div>
  </div>

<!--  Update Mode-->

</template>

<style scoped>
@import '../style/golf-user.css';
</style>
