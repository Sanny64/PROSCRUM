import { ref } from 'vue'
import type { Round } from '../types/types.ts'
import { result } from '../mockResultsData.json'
import {getToken} from "@/composables/token-administration.ts";
import type {Composer} from "vue-i18n";
import {i18n} from "@/main.ts";
import {useErrorController} from "@/composables/error-controller.ts";
const { setError } = useErrorController();




export function apiCallRounds() {
  const RoundsResult = ref<Round[]>([])

  async function getRoundsAPI() {
    try {
      const rawResponse = await fetch('http://localhost:8000/rounds', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json', // Setzt den Content-Type-Header
          authorization: "Bearer " + getToken(),

        },
      })

      if (!rawResponse.ok) {
        throw new Error(`HTTP-Fehler! Status: ${rawResponse.status}`)
      }

      const response = await rawResponse.json()

      RoundsResult.value = response
      console.log('1 Runden geladen:', RoundsResult.value)
    } catch (error) {
      console.error('getRoundsAPI:', error)
      const globalT = (i18n.global as Composer).t; //<---
      setError(globalT('error.users.permission_denied'));

    }
  }

  async function addRoundAPI(round: Round) {
    try {
      const rawResponse = await fetch('http://localhost:8000/rounds', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // Setzt den Content-Type-Header
          authorization: "Bearer " + getToken(),
        },
        body: JSON.stringify(round),
      })

      if (!rawResponse.ok) {
        throw new Error(`HTTP-Fehler! Status: ${rawResponse.status}`)
      }

      const response = await rawResponse.json()
      console.log('Kurs hinzugefügt:', response)

      RoundsResult.value = response.result
    } catch (error) {
      console.error('Fehler beim Hinzufügen des Kurses:', error)
    }
  }

  async function updateRoundAPI(round: Round) {
    try {
      const rawResponse = await fetch(`http://localhost:8000/rounds/${round.round_number}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json', // Setzt den Content-Type-Header
          authorization: "Bearer " + getToken(),
        },
        body: JSON.stringify(round),
      })

      if (!rawResponse.ok) {
        throw new Error(`HTTP-Fehler! Status: ${rawResponse.status}`)
      }

      const response = await rawResponse.json()
      console.log('Kurs aktualisiert:', response)

      RoundsResult.value = response.result
    } catch (error) {
      console.error('updateRoundAPI:', error)
      const globalT = (i18n.global as Composer).t; //<---
      setError(globalT('error.rounds.permission_denied'));
    }

  }

  async function deleteRoundAPI(round: Round) {
    try {
      const rawResponse = await fetch(`http://localhost:8000/rounds/${round.round_number}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json', // Setzt den Content-Type-Header
          authorization: "Bearer " + getToken(),
        },
      })

      if (!rawResponse.ok) {
        throw new Error(`HTTP-Fehler! Status: ${rawResponse.status}`)
      }

      const response = await rawResponse.json()
      console.log('Runde gelöscht:', response)

      RoundsResult.value = response.result
    } catch (error) {
      console.error('deleteRoundAPI', error)
      const globalT = (i18n.global as Composer).t; //<---
      setError(globalT('error.rounds.not_authorized'));
    }
  }

  return {
    apiResultRounds: RoundsResult,
    getRoundsAPI,
    addRoundAPI,
    updateRoundAPI,
    deleteRoundAPI,
  }
}
