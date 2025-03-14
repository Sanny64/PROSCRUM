import { ref } from 'vue'
import type {ScorecardInput, strokesAhead} from '../types/types.ts'
import {getToken} from './token-administration.ts'


export function getScorecard(){
  const strokes_ahead = ref<strokesAhead>()
  async function getStrokesAhead(scorecardValues: ScorecardInput) {
    try {
      const rawResponse = await fetch(`http://localhost:8000/scorecard?HDC=${scorecardValues.HDC}&course_id=${scorecardValues.course_id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // Setzt den Content-Type-Header
          authorization: "Bearer " + getToken(),
        }
      })

      if (!rawResponse.ok) {
        throw new Error('Fehler beim Holen der Schläge vorraus')
      }

      const response = await rawResponse.json()
      console.log('Scorecard response:', response)

      strokes_ahead.value = response.result
      console.log('strokes_ahead response:', strokes_ahead.value)
    } catch (error) {
      console.error('Fehler beim holen der Schläge vor:', error)
    }

  }

  return {
    apiResultScorecard: strokes_ahead,
    getStrokesAhead
  }
}
