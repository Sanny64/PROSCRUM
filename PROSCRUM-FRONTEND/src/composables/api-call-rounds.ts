import { ref } from 'vue'
import type { Round } from '../types/types.ts'
import { result } from '../mockResultsData.json'

export function apiCallRounds() {
  const RoundsResult = ref<Round[]>([])

  async function getRoundsAPI() {
    try {
      const rawResponse = await fetch('http://localhost:8000/rounds', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json', // Setzt den Content-Type-Header
        },
      })

      if (!rawResponse.ok) {
        throw new Error('Fehler beim Laden der Kurse')
      }

      const response = await rawResponse.json()

      RoundsResult.value = response.result
      console.log('1 Runden geladen:', RoundsResult.value)
    } catch (error) {
      console.error('Fehler beim Starten der Berechnung:', error)
    }
  }

  async function addRoundAPI(round: Round) {
    try {
      const rawResponse = await fetch('http://localhost:8000/courses', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // Setzt den Content-Type-Header
        },
        body: JSON.stringify(round),
      })

      if (!rawResponse.ok) {
        throw new Error('Fehler beim Hinzufügen des Kurses')
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
        },
        body: JSON.stringify(round),
      })

      if (!rawResponse.ok) {
        throw new Error('Fehler beim Aktualisieren des Kurses')
      }

      const response = await rawResponse.json()
      console.log('Kurs aktualisiert:', response)

      RoundsResult.value = response.result
    } catch (error) {
      console.error('Fehler beim Aktualisieren des Kurses:', error)
    }

  }

  async function deleteRoundAPI(round: Round) {
    try {
      const rawResponse = await fetch(`http://localhost:8000/rounds/${round.round_number}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json', // Setzt den Content-Type-Header
        },
      })

      if (!rawResponse.ok) {
        throw new Error('Fehler beim Löschen des Kurses')
      }

      const response = await rawResponse.json()
      console.log('Runde gelöscht:', response)

      RoundsResult.value = response.result
    } catch (error) {
      console.error('Fehler beim Löschen des Kurses:', error)
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
