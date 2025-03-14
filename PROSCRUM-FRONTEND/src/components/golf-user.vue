<script setup lang="ts">
import type {Round, User} from '../types/types.ts'
import {computed, defineEmits, onMounted, ref, watchEffect} from 'vue'
import {useI18n} from 'vue-i18n'
import {apiCallRounds} from '@/composables/api-call-rounds.ts'

const {} = apiCallRounds()


const { t } = useI18n()
const emit = defineEmits(['updated-user'])
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

const roles = computed(() => {
  return [
    {role_id: 1, role_name: t('usersPage.player')},
    {role_id: 2, role_name: t('usersPage.round_master')},
    {role_id: 3, role_name: t('usersPage.secretary')},
    {role_id: 4, role_name: t('usersPage.admin')}
  ]
})

const selectedRole = ref()





  onMounted(() => {
    selectedRole.value = props.user.role_id //<---
  })


function closeDetails() {
  gridView.value = true
}

function openDetails() {
  gridView.value = false
}

function updateRound() {
  editMode.value = false;
  gridView.value = true;
  props.user.role_id = selectedRole.value
  console.log('Send Emit', props.user)
  emit('updated-user', props.user)
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
      <form @submit.prevent="updateRound()">
              <div class="form-group">
                <label for="round">{{t('usersPage.email')}}</label>
                <b>{{props.user.email}}</b>
              </div>
              <div class="form-group">
                <label for="round">{{t('usersPage.created_at')}}</label>
                <b>{{props.user.created_at.split('T')[0]}}</b>
              </div>
              <div class="form-group">
                <label>{{ t('coursePage.secretaries') }}</label>
                <select v-model="selectedRole" class="dropdown-menu">
                  <option v-for="role in roles" :value="role.role_id" class="dropdown-item">
                    {{ role.role_name }}
                  </option>
                </select>
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
        <button type="submit" class="submit-btn">{{ t('roundPage.update') }}</button>
      <button class="submit-btn" @click="closeDetails()">{{ t('roundPage.close') }}</button>
      </form>
    </div>
  </div>



</template>

<style scoped>
@import '../style/golf-user.css';
</style>
