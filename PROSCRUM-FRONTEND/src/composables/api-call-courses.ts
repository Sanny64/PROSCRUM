import { ref } from 'vue'
import type { Course, CourseWithoutID } from '../types/types.ts'

export function apiCallCourses() {
  const CourseResult = ref<Course[]>([])

  async function getCoursesAPI() {
    try {
      const rawResponse = await fetch('http://localhost:8000/courses', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json', // Setzt den Content-Type-Header
        },
      })

      if (!rawResponse.ok) {
        throw new Error('Fehler beim Laden der Kurse')
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
        },
        body: JSON.stringify(course),
      })

      if (!rawResponse.ok) {
        throw new Error('Fehler beim Hinzufügen des Kurses')
      }

      const response = await rawResponse.json()
      console.log('Kurs hinzugefügt:', response)

      CourseResult.value = response.result
    } catch (error) {
      console.error('Fehler beim Hinzufügen des Kurses:', error)
    }
  }

  async function deleteCourseAPI(course: Course) {
    try {
      const rawResponse = await fetch(`http://localhost:8000/courses/${course.course_id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json', // Setzt den Content-Type-Header
        },
      })

      if (!rawResponse.ok) {
        throw new Error('Fehler beim Löschen des Kurses')
      }

      const response = await rawResponse.status
      console.log('Kurs gelöscht:', response)
    } catch (error) {
      console.error('Fehler beim Löschen des Kurses:', error)
    }
  }

  return {
    apiResultCourse: CourseResult,
    getCoursesAPI,
    addCourseAPI,
    deleteCourseAPI,
  }
}
