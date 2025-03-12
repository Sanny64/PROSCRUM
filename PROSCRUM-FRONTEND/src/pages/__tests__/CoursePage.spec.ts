import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { shallowMount } from '@vue/test-utils'
import CoursePage from '../CoursePage.vue'
import { createI18n } from 'vue-i18n'
import { ref, nextTick } from 'vue'

// 🔹 Mock-Funktionen für API-Aufrufe
const getCoursesAPIMock = vi.fn()
const addCourseAPIMock = vi.fn()
const deleteCourseAPIMock = vi.fn()

// 🔹 Mock für `apiCallCourses`
const apiResultCourse = ref([]) // Leere Course-Liste als Startwert

vi.mock('@/composables/api-call-courses.ts', () => ({
  apiCallCourses: vi.fn(() => ({
    apiResultCourse, // Leere Course-Liste als Startwert
    getCoursesAPI: getCoursesAPIMock,
    addCourseAPI: addCourseAPIMock,
    deleteCourseAPI: deleteCourseAPIMock,
  })),
}))

import { apiCallCourses } from '@/composables/api-call-courses'

// 🔹 i18n für Tests mit englischer Übersetzung
export const i18n = createI18n({
  legacy: false,
  locale: 'en',
  messages: {
    en: {
      coursePage: {
        courseName: 'Course name: ',
        par: 'Par: ',
        courseRating: 'Course Rating: ',
        slopeRating: 'Slope Rating: ',
        hole: 'Hole: ',
        hdc: 'HDC.: ',
        save: 'Save',
        delete: 'Delete',
        close: 'Close',
      },
    },
  },
})

describe('CoursePage.vue', () => {
  let wrapper: ReturnType<typeof shallowMount>

  beforeEach(() => {
    vi.clearAllMocks()
    wrapper = shallowMount(CoursePage, {
      global: { plugins: [i18n] },
    })
  })

  afterEach(() => {
    wrapper.unmount()
  })

  // ✅ Test: Die Komponente sollte ohne Fehler gerendert werden
  it('should render the CoursePage component', () => {
    expect(wrapper.exists()).toBe(true)
  })

  // ✅ Test: CourseFilter wird korrekt gerendert
  it('should render CourseFilter component', () => {
    const filterComponent = wrapper.findComponent({ name: 'CourseFilter' })
    expect(filterComponent.exists()).toBe(true)
    expect(filterComponent.props('courseList')).toEqual([])
  })

  // ✅ Test: AddGolfCourse wird korrekt gerendert
  it('should render AddGolfCourse component', () => {
    const addCourseComponent = wrapper.findComponent({ name: 'AddGolfCourse' })
    expect(addCourseComponent.exists()).toBe(true)
  })

  // ✅ Test: GolfCourse-Komponenten werden für gefilterte Courses gerendert
  it('should render GolfCourse components for filteredCourseList', async () => {
    const { apiResultCourse } = apiCallCourses()

    apiResultCourse.value = [
      {
        course_name: 'Sunny Hills Golf Course',
        course_par: 72,
        course_rating_9: null,
        course_rating_18: 70.9,
        slope_rating: 115,
        holes: [
          { hole: 1, par: 3, hdc: 4 },
          { hole: 2, par: 4, hdc: 16 },
          { hole: 3, par: 4, hdc: 1 },
          { hole: 4, par: 5, hdc: 10 },
          { hole: 5, par: 4, hdc: 7 },
          { hole: 6, par: 4, hdc: 13 },
          { hole: 7, par: 3, hdc: 5 },
          { hole: 8, par: 4, hdc: 17 },
          { hole: 9, par: 4, hdc: 2 },
          { hole: 10, par: 5, hdc: 11 },
          { hole: 11, par: 4, hdc: 8 },
          { hole: 12, par: 4, hdc: 14 },
          { hole: 13, par: 3, hdc: 6 },
          { hole: 14, par: 4, hdc: 18 },
          { hole: 15, par: 4, hdc: 3 },
          { hole: 16, par: 5, hdc: 12 },
          { hole: 17, par: 4, hdc: 9 },
          { hole: 18, par: 4, hdc: 15 },
        ],
        course_id: 1,
      },
      {
        course_name: 'Shady Hills Golf Course',
        course_par: 68,
        course_rating_9: null,
        course_rating_18: 72.3,
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
          { hole: 18, par: 4, hdc: 6 },
        ],
        course_id: 2,
      },
      {
        course_name: 'Cedar Ridge Golf Course',
        course_par: 35,
        course_rating_9: 34.1,
        course_rating_18: 74.1,
        slope_rating: 115,
        holes: [
          { hole: 1, par: 3, hdc: 4 },
          { hole: 2, par: 4, hdc: 16 },
          { hole: 3, par: 4, hdc: 1 },
          { hole: 4, par: 5, hdc: 10 },
          { hole: 5, par: 4, hdc: 7 },
          { hole: 6, par: 4, hdc: 13 },
          { hole: 7, par: 3, hdc: 5 },
          { hole: 8, par: 4, hdc: 17 },
          { hole: 9, par: 4, hdc: 2 },
        ],
        course_id: 3,
      },
      {
        course_name: 'Sunny Hills Golf Course',
        course_par: 35,
        course_rating_9: 35.7,
        course_rating_18: 70.1,
        slope_rating: 130,
        holes: [
          { hole: 1, par: 3, hdc: 4 },
          { hole: 2, par: 4, hdc: 16 },
          { hole: 3, par: 4, hdc: 1 },
          { hole: 4, par: 5, hdc: 10 },
          { hole: 5, par: 4, hdc: 7 },
          { hole: 6, par: 4, hdc: 13 },
          { hole: 7, par: 3, hdc: 5 },
          { hole: 8, par: 4, hdc: 17 },
          { hole: 9, par: 4, hdc: 2 },
        ],
        course_id: 4,
      },
    ]

    await nextTick()

    const courseComponents = wrapper.findAllComponents({ name: 'GolfCourse' })
    expect(courseComponents.length).toBe(4)
  })

  // ✅ Test: `getCoursesAPI()` wird beim Mounten aufgerufen
  it('should call getCoursesAPI on mount', () => {
    expect(getCoursesAPIMock).toHaveBeenCalled()
  })

  // ✅ Test: `addCourseAPI()` wird aufgerufen, wenn ein neuer Course hinzugefügt wird
  it('should call addCourseAPI when a course is added', async () => {
    const addCourseComponent = wrapper.findComponent({ name: 'AddGolfCourse' })

    addCourseComponent.vm.$emit('course-added', {
      course_name: 'New Course',
      course_rating_18: 70,
      slope_rating: 115,
    })

    await nextTick()

    expect(addCourseAPIMock).toHaveBeenCalledWith({
      course_name: 'New Course',
      course_rating_18: 70,
      slope_rating: 115,
    })

    expect(getCoursesAPIMock).toHaveBeenCalled()
  })

  // // ✅ Test: `deleteCourseAPI()` wird aufgerufen, wenn ein Course gelöscht wird
  // it("should call deleteCourseAPI when a course is deleted", async () => {
  //   const { apiResultCourse } = apiCallCourses()
  //   ;
  //
  //   await nextTick();
  //
  //   const courseComponent = wrapper.findComponent({ name: "GolfCourse" });
  //
  //   courseComponent.vm.$emit("course-deleted", { course_id: 1 });
  //
  //   await nextTick();
  //
  //   expect(deleteCourseAPIMock).toHaveBeenCalledWith({ course_id: 1 });
  //   expect(getCoursesAPIMock).toHaveBeenCalled();
  // });

  // ✅ Test: `filterCourses()` aktualisiert `filteredCourseList`
  // it("should update filteredCourseList when filters change", async () => {
  //   const filterComponent = wrapper.findComponent({ name: "CourseFilter" });
  //
  //   filterComponent.vm.$emit("text-value", "test");
  //   filterComponent.vm.$emit("course-rating-value", 70);
  //   filterComponent.vm.$emit("slope-rating-value", 115);
  //
  //   await nextTick();
  //
  //   expect(wrapper.vm.inputValue).toBe("test");
  //   expect(wrapper.vm.courseRatingValue).toBe(70);
  //   expect(wrapper.vm.slopeRatingValue).toBe(115);
  //
  // });
})
