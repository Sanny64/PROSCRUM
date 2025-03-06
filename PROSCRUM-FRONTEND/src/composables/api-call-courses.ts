import { ref } from 'vue'
import type { Course, CourseWithoutID } from '../types/types.ts'

export function apiCallCourses() {
  const CourseResult = ref<Course[]>([{
    course_id: 1,
    course_name: "Platz am See",
    course_par_1_to_9: null,
    course_par_10_to_18: null,
    course_par_all: 72,
    course_rating_1_to_9: null,
    course_rating_10_to_18: null,
    course_rating_all: 72.3,
    slope_rating: 130,
    holes: [
      { hole: 1, par: 3, hdc: 16 },
      { hole: 2, par: 4, hdc: 1 },
      { hole: 3, par: 4, hdc: 10 },
      { hole: 4, par: 5, hdc: 7 },
      { hole: 5, par: 4, hdc: 13 },
      { hole: 6, par: 4, hdc: 4 },
      { hole: 7, par: 3, hdc: 17 },
      { hole: 8, par: 4, hdc: 2 },
      { hole: 9, par: 4, hdc: 11 },
      { hole: 10, par: 5, hdc: 8 },
      { hole: 11, par: 4, hdc: 14 },
      { hole: 12, par: 4, hdc: 5 },
      { hole: 13, par: 3, hdc: 18 },
      { hole: 14, par: 4, hdc: 3 },
      { hole: 15, par: 4, hdc: 12 },
      { hole: 16, par: 5, hdc: 9 },
      { hole: 17, par: 4, hdc: 15 },
      { hole: 18, par: 4, hdc: 6 }
    ]
  },
    {
    course_id: 2,
    course_name: "Leichte Prise",
    course_par_1_to_9: 30,
    course_par_10_to_18: null,
    course_par_all: 72,
    course_rating_1_to_9: 40,
    course_rating_10_to_18: null,
    course_rating_all: 72.3,
    slope_rating: 130,
    holes: [
      { hole: 1, par: 3, hdc: 16 },
      { hole: 2, par: 4, hdc: 1 },
      { hole: 3, par: 4, hdc: 10 },
      { hole: 4, par: 5, hdc: 7 },
      { hole: 5, par: 4, hdc: 13 },
      { hole: 6, par: 4, hdc: 4 },
      { hole: 7, par: 3, hdc: 17 },
      { hole: 8, par: 4, hdc: 2 },
      { hole: 9, par: 4, hdc: 11 },
      { hole: 10, par: 5, hdc: 8 },
      { hole: 11, par: 4, hdc: 14 },
      { hole: 12, par: 4, hdc: 5 },
      { hole: 13, par: 3, hdc: 18 },
      { hole: 14, par: 4, hdc: 3 },
      { hole: 15, par: 4, hdc: 12 },
      { hole: 16, par: 5, hdc: 9 },
      { hole: 17, par: 4, hdc: 15 },
      { hole: 18, par: 4, hdc: 6 }
    ]
  },
    {
    course_id: 3,
    course_name: "Schwerer Brocken",
    course_par_1_to_9: 10,
    course_par_10_to_18: 15,
    course_par_all: 72,
    course_rating_1_to_9: 20,
    course_rating_10_to_18: 30,
    course_rating_all: 72.3,
    slope_rating: 130,
    holes: [
      { hole: 1, par: 3, hdc: 16 },
      { hole: 2, par: 4, hdc: 1 },
      { hole: 3, par: 4, hdc: 10 },
      { hole: 4, par: 5, hdc: 7 },
      { hole: 5, par: 4, hdc: 13 },
      { hole: 6, par: 4, hdc: 4 },
      { hole: 7, par: 3, hdc: 17 },
      { hole: 8, par: 4, hdc: 2 },
      { hole: 9, par: 4, hdc: 11 },
      { hole: 10, par: 5, hdc: 8 },
      { hole: 11, par: 4, hdc: 14 },
      { hole: 12, par: 4, hdc: 5 },
      { hole: 13, par: 3, hdc: 18 },
      { hole: 14, par: 4, hdc: 3 },
      { hole: 15, par: 4, hdc: 12 },
      { hole: 16, par: 5, hdc: 9 },
      { hole: 17, par: 4, hdc: 15 },
      { hole: 18, par: 4, hdc: 6 }
    ]
  }])

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
