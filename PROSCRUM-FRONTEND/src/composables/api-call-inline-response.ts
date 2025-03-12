import { ref } from 'vue'
import type { FormData, CalculationResult } from '../types/types.ts'
import {getToken} from './token-administration.ts'


export function apiCallInlineResponse() {
  const inlineStatus = ref<number>()
  const inlineResult = ref<CalculationResult | null | undefined>()

  async function sendFormdata(input: FormData) {
    inlineStatus.value = 199
    try {
      const rawResponse = await fetch('http://localhost:8000/rounds', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // Setzt den Content-Type-Header
          authorization: 'Bearer ' + getToken(),
        },
        body: JSON.stringify(input),
      })

      if (!rawResponse.ok) {
        throw new Error('Fehler beim Starten der Berechnung')
      }

      const response = await rawResponse.status
      console.log('Berechnung gestartet:', response)

      inlineStatus.value = response
    } catch (error) {
      console.error('Fehler beim Starten der Berechnung:', error)
    }
  }

  return {
    apiStatus: inlineStatus,
    apiResult: inlineResult,
    sendFormdata,
  }
}
