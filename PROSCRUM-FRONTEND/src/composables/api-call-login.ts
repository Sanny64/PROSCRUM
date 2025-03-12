import { ref } from 'vue'
import {setToken,} from './token-administration.ts'
import type { LoginData } from '../types/types.ts'




export async function apiCallLogin() {

  const loginData: LoginData = {
    username: 'robin@test.de',
    password: '1234'
  }

  const formData = new FormData();
  formData.append("username", loginData.username)
  formData.append("password", loginData.password)


  console.log("SendFormat data:" + formData.)
  try {
    const rawResponse = await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: {
        'content-type':'application/x-www-form-urlencoded', // Setzt den Content-Type-Header
      },
      body: formData,
    })

    if (!rawResponse.ok) {
      throw new Error('Fehler beim Login')
    }

    const response = await rawResponse.json()

    console.log('2: Token erhalten:', response)
    setToken(response.access_token);

  } catch (error) {
    console.error('Fehler beim Login:', error)
  }
}
