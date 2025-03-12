import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount, shallowMount } from '@vue/test-utils'
import HomePage from '../HomePage.vue'
import { createI18n } from 'vue-i18n'
import { nextTick, ref } from 'vue'

const getCoursesAPIMock = vi.fn() // Mock für `getCoursesAPI`
const getRoundsAPIMock = vi.fn() // Mock für `getRoundsAPI`
const sendFormdataMock = vi.fn()

const apiStatus = ref(199)

vi.mock('@/composables/api-call-inline-response.ts', () => ({
  apiCallInlineResponse: vi.fn(() => ({
    apiStatus,
    sendFormdata: sendFormdataMock,
  })),
}))

vi.mock('@/composables/api-call-courses.ts', () => ({
  apiCallCourses: vi.fn(() => ({
    apiResultCourse: ref([]),
    getCoursesAPI: getCoursesAPIMock, // ✅ Mock-Funktion verwenden
  })),
}))

vi.mock('@/composables/api-call-rounds.ts', () => ({
  apiCallRounds: vi.fn(() => ({
    apiResultRounds: ref([]),
    getRoundsAPI: getRoundsAPIMock, // ✅ Mock-Funktion verwenden
  })),
}))

import { apiCallInlineResponse } from '@/composables/api-call-inline-response'

// 🔹 i18n für Tests mit englischer Übersetzung
export const i18n = createI18n({
  legacy: false, // Für Composition API
  locale: 'en', // Standard-Sprache
  messages: {
    en: {
      title: 'Golf Handicap Calculator',
      home: 'Home',
      course: 'Course',
      rounds: 'Rounds',
      login: 'Login',
      signup: 'Sign up',
      input: {
        input: 'Input',
        round: 'Round: ',
        courseRating: 'Course Rating: ',
        slopeRating: 'Slope Rating: ',
        courseSelection: 'Select a course',
        holes: 'Holes',
        hole: '. Hole: ',
        calculate: 'Calculate',
      },
      output: {
        output: 'Output',
        yourCurrentHandicap: 'Your current handicap:',
        until2021: 'until 2020: ',
        from2021: 'from 2021: ',
        results: 'Results',
        until2021Chart: 'Until 2020',
        from2021Chart: 'From 2021',
        round: 'Round',
        rounds: 'Rounds',
        resultsFrom2021: 'Results from 2021',
        resultsUntil2020: 'Results until 2020',
        scoreDifferential: 'Score Differential',
        more: 'More',
        fewer: 'Fewer',
      },
    },
  },
})

describe('HomePage.vue', () => {
  let wrapper: ReturnType<typeof shallowMount>

  beforeEach(() => {
    vi.restoreAllMocks()
    wrapper = shallowMount(HomePage, {
      global: { plugins: [i18n] },
    })
  })

  afterEach(() => {
    wrapper.unmount() // 🔹 Entfernt die Komponente nach jedem Test
  })

  // ✅ Test: Die Komponente sollte ohne Fehler gerendert werden
  it('should render the HomePage component', () => {
    console.log(wrapper.html()) // Debugging: Gibt das gerenderte HTML aus
    expect(wrapper.exists()).toBe(true) // ✅ Prüft, ob die Komponente existiert
  })

  // ✅ Test: Die `CalculationInput`-Komponente sollte vorhanden sein
  it('should render CalculationInput component', () => {
    const inputComponent = wrapper.findComponent({ name: 'CalculationInput' })
    expect(inputComponent.exists()).toBe(true) // ✅ Prüft, ob `CalculationInput` existiert
  })

  // ✅ Test: Die `CalculationOutput`-Komponente sollte vorhanden sein
  it('should render CalculationOutput component', () => {
    const outputComponent = wrapper.findComponent({ name: 'CalculationOutput' })
    expect(outputComponent.exists()).toBe(true) // ✅ Prüft, ob `CalculationOutput` existiert
  })

  it('should call getCoursesAPI and getRoundsAPI on mount', () => {
    expect(getCoursesAPIMock).toHaveBeenCalled()
    expect(getRoundsAPIMock).toHaveBeenCalled()
  })

  // ✅ Test: `sendFormdata` sollte aufgerufen werden, wenn `formData` von `CalculationInput` emittiert wird
  it('should call sendFormdata when CalculationInput emits formData', async () => {
    const inputComponent = wrapper.findComponent({ name: 'CalculationInput' })

    // 🔹 Event auslösen
    inputComponent.vm.$emit('formData', { name: 'Test' })

    // ✅ Test: Wurde `sendFormdata()` mit `formData` aufgerufen?
    expect(sendFormdataMock).toHaveBeenCalledWith({ name: 'Test' })
  })

  it('should call getRoundsAPI when apiStatus is set to 201', async () => {
    const { apiStatus } = apiCallInlineResponse()
    apiStatus.value = 201

    await nextTick()

    expect(getRoundsAPIMock).toHaveBeenCalledTimes(2)
  })
})
