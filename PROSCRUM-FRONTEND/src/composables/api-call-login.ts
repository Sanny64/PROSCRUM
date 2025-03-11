import { ref } from 'vue'
import {setToken,} from './token-administration.ts'
import type { LoginData } from '../types/types.ts'



export function apiCallLogin(loginData: LoginData) {

    try {
      // const rawResponse = await fetch('http://localhost:8000/login', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json', // Setzt den Content-Type-Header
      //   },
      //   body: JSON.stringify(loginData),
      // })
      //
      // if (!rawResponse.ok) {
      //   throw new Error('Fehler beim Hinzufügen des Kurses')
      // }

      // const response = await rawResponse.json()
      const response = {
        token_type:"Bearer",}
      console.log('2: Token erhalten:', response)
      setToken(response.access_token);

    } catch (error) {
      console.error('Fehler beim Hinzufügen des Kurses:', error)
    }
}
