import type {DecodedToken, User, UserCreate} from '../types/types.ts';
import {getToken} from './token-administration.ts'
import {jwtDecode} from "jwt-decode";

export function apiCallUser() {


  async function getActiveUserAPI() {
    try {
      const decodedToken: DecodedToken = jwtDecode<DecodedToken>(getToken());
      // const rawResponse = await fetch(`http://localhost:8000/user/${decodedToken.role_id}`, {
      //   method: "GET",
      //   headers: {
      //     "Content-Type": "application/json",
      //     authorization: "Bearer " + getToken(),
      //   },
      // });
      //
      // if (!rawResponse.ok) {
      //   throw new Error('Fehler beim Laden der Kurse')
      // }
      //
      // const response = await rawResponse.json()
      console.log('4: Kurse geladen:', {
        first_name: "Jakob",
        last_name: "Kraus",
        user_id: decodedToken.role_id,
        email: "jakobfischer@gmail.com",
        role_id: 1,
        created_at: "2021-05-12T12:00:00Z",
      })
      return {
        first_name: "Jakob",
        last_name: "Kraus",
        user_id: decodedToken.role_id,
        email: "jakobfischer@gmail.com",
        role_id: 1,
        created_at: "2021-05-12T12:00:00Z",
      }
    } catch (error) {
      console.error('Fehler beim Starten der Berechnung:', error)
      return "INVALID"
    }
  }


  async function getUserAPI(user_id: number) {
    try {
      const rawResponse = await fetch(`http://localhost:8000/user/${user_id}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          authorization: "Bearer " + getToken(),
        },
      });

      if (!rawResponse.ok) {
        throw new Error('Fehler beim Laden der Kurse')
      }

      const response = await rawResponse.json()
      console.log('Kurse geladen:', response)

      return response
    } catch (error) {
      console.error('Fehler beim Starten der Berechnung:', error)
    }
  }

  async function addUserAPI(user: UserCreate) {
    console.log('sendFormdata', JSON.stringify(user))

    try {
      const rawResponse = await fetch('http://localhost:8000/user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          authorization: "Bearer " + getToken(),
        },
        body: JSON.stringify(user),
      })

      if (!rawResponse.ok) {
        throw new Error('Fehler beim Hinzufügen des Kurses')
      }

      const response = await rawResponse.json()
      console.log('Kurs hinzugefügt:', response)

    } catch (error) {
      console.error('Fehler beim Hinzufügen des Users:', error)
    }
  }

  async function deleteUserAPI(user_id: number) {
    try {
      const rawResponse = await fetch(`http://localhost:8000/user/${user_id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json', // Setzt den Content-Type-Header
        },
      })

      if (!rawResponse.ok) {
        throw new Error('Fehler beim Löschen des Kurses')
      }

      const response = rawResponse.status
      console.log('Kurs gelöscht:', response)
    } catch (error) {
      console.error('Fehler beim Löschen des Kurses:', error)
    }
  }

  return {
    getActiveUserAPI,
    getUserAPI,
    addUserAPI,
    deleteUserAPI
  }
}
