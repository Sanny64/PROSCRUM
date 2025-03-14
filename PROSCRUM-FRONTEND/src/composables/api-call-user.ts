import type {DecodedToken, User, UserCreate} from '../types/types.ts';
import {getToken} from './token-administration.ts'
import {jwtDecode} from "jwt-decode";
import {ref} from "vue";
import {i18n} from "@/main.ts";
import type {Composer} from "vue-i18n";
import {useErrorController} from "@/composables/error-controller.ts";

const { setError } = useErrorController();

export function apiCallUser() {

  const activeUserAPI= ref<User|'INVALID'>('INVALID')
  const allUserList= ref<User[]>([])


  async function getActiveUserAPI() {
    try {
      const decodedToken: DecodedToken = jwtDecode<DecodedToken>(getToken());
      console.log('3: Token dekodiert:', decodedToken)
      const rawResponse = await fetch(`http://localhost:8000/users/${decodedToken.user_id}`, {
        method: "GET",
        headers: {
          authorization: "Bearer " + getToken(),
        },
      });
      if (!rawResponse.ok) {
        throw new Error(`HTTP-Fehler! Status: ${rawResponse.status}`)
      }

      const response = await rawResponse.json()
      console.log('4: Kurse geladen:', response)
      activeUserAPI.value = response
    } catch (error) {
      console.error('getActiveUserAPI', error)
      const globalT = (i18n.global as Composer).t; //<---
      setError(globalT('error.users.permission_denied'));
      activeUserAPI.value = 'INVALID';
      return;
    }
  }


  async function getUserAPI(user_id: number) {
    try {
      const rawResponse = await fetch(`http://localhost:8000/users/${user_id}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          authorization: "Bearer " + getToken(),
        },
      });

      if (!rawResponse.ok) {
        throw new Error(`HTTP-Fehler! Status: ${rawResponse.status}`)
      }

      const response = await rawResponse.json()
      console.log('Kurse geladen:', response)

      return response
    } catch (error) {
      console.error('getUserAPI:', error)
      const globalT = (i18n.global as Composer).t; //<---
      setError(globalT('error.users.permission_denied'));
    }
  }

  async function getUserAllAPI() {
    try {
      const rawResponse = await fetch(`http://localhost:8000/users`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          authorization: "Bearer " + getToken(),
        },
      });

      if (!rawResponse.ok) {
        throw new Error(`HTTP-Fehler! Status: ${rawResponse.status}`)
      }

      allUserList.value = await rawResponse.json()
      console.log('All User:', allUserList.value)


    } catch (error) {
      console.error('getUserAllAPI:', error)
      const globalT = (i18n.global as Composer).t; //<---
      setError(globalT('error.users.permission_denied'));
    }
  }

  async function addUserAPI(user: UserCreate) {
    console.log('sendFormdata', JSON.stringify(user))

    try {
      const rawResponse = await fetch('http://localhost:8000/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          authorization: "Bearer " + getToken(),
        },
        body: JSON.stringify(user),
      })

      if (!rawResponse.ok) {
        throw new Error(`HTTP-Fehler! Status: ${rawResponse.status}`)
      }

      return await rawResponse.json()

    } catch (error) {
      console.error('addUserAPI:', error)
    }
  }

  async function updateUserAPI(user: User) {
    console.log('sendFormdata', JSON.stringify(user))

    try {
      const rawResponse = await fetch(`http://localhost:8000/users/${user.user_id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          authorization: "Bearer " + getToken(),
        },
        body: JSON.stringify(user),
      })

      if (!rawResponse.ok) {
        throw new Error(`HTTP-Fehler! Status: ${rawResponse.status}`)
      }

      return await rawResponse.json()

    } catch (error) {
      console.error('updateUserAPI:', error)
      const globalT = (i18n.global as Composer).t;
      setError(globalT('error.users.not_authorized'));
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
      console.error('deleteUserAPI:', error)
      const globalT = (i18n.global as Composer).t;
      setError(globalT('error.users.not_authorized'));
    }
  }

  return {
    allUserList,
    activeUserAPI,
    getActiveUserAPI,
    getUserAllAPI,
    getUserAPI,
    addUserAPI,
    deleteUserAPI,
    updateUserAPI
  }
}
