import { ref } from 'vue'
import type { Course, CourseWithoutID } from '../types/types.ts'
import {getToken} from "@/composables/token-administration.ts";
import type {Composer} from "vue-i18n";
import {i18n} from "@/main.ts";
import {useErrorController} from "@/composables/error-controller.ts";

const { setError } = useErrorController();

export function apiCallCourses() {
  const CourseResult = ref<Course[]>([])

  async function getCoursesAPI() {
    try {
      const rawResponse = await fetch('http://localhost:8000/courses', {
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
      console.log('Kurse geladen:', response)

      CourseResult.value = response.result
    } catch (error) {
      console.error('Fehler beim Starten der Berechnung:', error)
    }
  }

  async function addCourseAPI(course: CourseWithoutID) {
    console.log('sendFormdata', JSON.stringify(course))

    try {
      const rawResponse = await fetch('http://localhost:8000/courses', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // Setzt den Content-Type-Header
          authorization: "Bearer " + getToken(),
        },
        body: JSON.stringify(course),
      })

      if (!rawResponse.ok) {
        throw new Error(`HTTP-Fehler! Status: ${rawResponse.status}`)
      }

      const response = await rawResponse.json()
      console.log('Kurs hinzugefügt:', response)

      CourseResult.value = response.result
    } catch (error) {
      console.error('addCourseAPI:', error)
      const globalT = (i18n.global as Composer).t; //<---
      setError(globalT('error.course.permission_denied'));
    }
  }

  async function deleteCourseAPI(course: Course) {
    try {
      const rawResponse = await fetch(`http://localhost:8000/courses/${course.course_id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json', // Setzt den Content-Type-Header
          authorization: "Bearer " + getToken(),

        },
      })

      if (!rawResponse.ok) {
        throw new Error(`HTTP-Fehler! Status: ${rawResponse.status}`)
      }

      const response = await rawResponse.status
      console.log('Kurs gelöscht:', response)
    } catch (error) {
      console.error('deleteCourseAPI:', error)
      const globalT = (i18n.global as Composer).t; //<---
      setError(globalT('error.course.not_authorized'));
    }
  }

  return {
    apiResultCourse: CourseResult,
    getCoursesAPI,
    addCourseAPI,
    deleteCourseAPI,
  }
}
