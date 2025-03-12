import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { shallowMount } from '@vue/test-utils'
import CalculationOutput from '../calculation-output.vue'
import { createI18n } from 'vue-i18n'
import type { Round } from '../../types/types'

// 🔹 i18n für Tests mit englischer Übersetzung
export const i18n = createI18n({
  legacy: false,
  locale: 'en',
  messages: {
    en: {
      output: {
        output: 'Output',
        yourCurrentHandicap: 'Your current handicap:',
        until2021: 'until 2020: ',
        from2021: 'from 2021: ',
      },
    },
  },
})

// 🔹 Mock-Daten für Runden
const mockRoundsResult: Round[] = [
  {
    round_number: 1,
    course: {
      course_name: 'Sunny Hills Golf Course',
      course_par: 72,
      course_rating_9: null,
      course_rating_18: 70.9,
      slope_rating: 115,
      holes: [
        {
          hole: 1,
          par: 3,
          hdc: 4,
        },
        {
          hole: 2,
          par: 4,
          hdc: 16,
        },
        {
          hole: 3,
          par: 4,
          hdc: 1,
        },
        {
          hole: 4,
          par: 5,
          hdc: 10,
        },
        {
          hole: 5,
          par: 4,
          hdc: 7,
        },
        {
          hole: 6,
          par: 4,
          hdc: 13,
        },
        {
          hole: 7,
          par: 3,
          hdc: 5,
        },
        {
          hole: 8,
          par: 4,
          hdc: 17,
        },
        {
          hole: 9,
          par: 4,
          hdc: 2,
        },
        {
          hole: 10,
          par: 5,
          hdc: 11,
        },
        {
          hole: 11,
          par: 4,
          hdc: 8,
        },
        {
          hole: 12,
          par: 4,
          hdc: 14,
        },
        {
          hole: 13,
          par: 3,
          hdc: 6,
        },
        {
          hole: 14,
          par: 4,
          hdc: 18,
        },
        {
          hole: 15,
          par: 4,
          hdc: 3,
        },
        {
          hole: 16,
          par: 5,
          hdc: 12,
        },
        {
          hole: 17,
          par: 4,
          hdc: 9,
        },
        {
          hole: 18,
          par: 4,
          hdc: 15,
        },
      ],
      course_id: 1,
    },
    scores: [5, 6, 8, 7, 6, 6, 6, 6, 6, 7, 6, 6, 5, 6, 6, 6, 5, 6],
    calc_result_2020: 53.9,
    calc_result_2021: 35.4,
    score_differential: 37.4,
  },
  {
    round_number: 2,
    course: {
      course_name: 'Sunny Hills Golf Course',
      course_par: 72,
      course_rating_9: null,
      course_rating_18: 70.9,
      slope_rating: 115,
      holes: [
        {
          hole: 1,
          par: 3,
          hdc: 4,
        },
        {
          hole: 2,
          par: 4,
          hdc: 16,
        },
        {
          hole: 3,
          par: 4,
          hdc: 1,
        },
        {
          hole: 4,
          par: 5,
          hdc: 10,
        },
        {
          hole: 5,
          par: 4,
          hdc: 7,
        },
        {
          hole: 6,
          par: 4,
          hdc: 13,
        },
        {
          hole: 7,
          par: 3,
          hdc: 5,
        },
        {
          hole: 8,
          par: 4,
          hdc: 17,
        },
        {
          hole: 9,
          par: 4,
          hdc: 2,
        },
        {
          hole: 10,
          par: 5,
          hdc: 11,
        },
        {
          hole: 11,
          par: 4,
          hdc: 8,
        },
        {
          hole: 12,
          par: 4,
          hdc: 14,
        },
        {
          hole: 13,
          par: 3,
          hdc: 6,
        },
        {
          hole: 14,
          par: 4,
          hdc: 18,
        },
        {
          hole: 15,
          par: 4,
          hdc: 3,
        },
        {
          hole: 16,
          par: 5,
          hdc: 12,
        },
        {
          hole: 17,
          par: 4,
          hdc: 9,
        },
        {
          hole: 18,
          par: 4,
          hdc: 15,
        },
      ],
      course_id: 1,
    },
    scores: [4, 5, 5, 6, 6, 5, 6, 9, 5, 5, 6, 6, 5, 6, 6, 6, 5, 6],
    calc_result_2020: 53.8,
    calc_result_2021: 28.6,
    score_differential: 30.6,
  },
]

describe('CalculationOutput.vue', () => {
  let wrapper: ReturnType<typeof shallowMount>

  beforeEach(() => {
    vi.clearAllMocks()
    wrapper = shallowMount(CalculationOutput, {
      global: { plugins: [i18n] },
      props: {
        pollingStatus: undefined,
        roundsResult: mockRoundsResult,
      },
    })
  })

  afterEach(() => {
    wrapper.unmount()
  })

  // ✅ Test: Komponente sollte ohne Fehler gerendert werden
  it('should render the CalculationOutput component', () => {
    expect(wrapper.exists()).toBe(true)
  })

  // ✅ Test: Überschriften sollten korrekt gerendert werden
  it('should render the correct headings', () => {
    expect(wrapper.find('h1').text()).toBe('Output')
    expect(wrapper.find('h2').text()).toBe('Your current handicap:')
  })

  // ✅ Test: Die berechneten Ergebnisse sollten korrekt angezeigt werden
  it('should display the correct calculated results', () => {
    const calcOutputs = wrapper.findAll('.calcOutput')

    expect(calcOutputs.at(0)?.text()).toContain('until 2020: ')
    expect(calcOutputs.at(0)?.find('b')?.text()).toBe('53.8') // Letzter Wert aus mockRoundsResult

    expect(calcOutputs.at(1)?.text()).toContain('from 2021: ')
    expect(calcOutputs.at(1)?.find('b')?.text()).toBe('28.6') // Letzter Wert aus mockRoundsResult
  })

  // ✅ Test: Das Lade-GIF sollte angezeigt werden, wenn pollingStatus 199 ist
  it('should display loading GIF when pollingStatus is 199', async () => {
    await wrapper.setProps({ pollingStatus: 199 })

    expect(wrapper.find('.loadingGif').exists()).toBe(true)
    expect(wrapper.find('.loadingGif img').attributes('alt')).toBe('loading-gif')
  })

  // ✅ Test: Runden-Chart und -Tabelle sollten gerendert werden, wenn Runden-Daten vorhanden sind
  it('should render rounds-chart and rounds-table when roundsResult has data', () => {
    expect(wrapper.findComponent({ name: 'RoundsChart' }).exists()).toBe(true)
    expect(wrapper.findComponent({ name: 'RoundsTable' }).exists()).toBe(true)
  })

  // ✅ Test: Runden-Chart und -Tabelle sollten nicht gerendert werden, wenn keine Runden-Daten vorhanden sind
  it('should not render rounds-chart and rounds-table when roundsResult is empty', async () => {
    await wrapper.setProps({ roundsResult: [] })

    expect(wrapper.findComponent({ name: 'RoundsChart' }).exists()).toBe(false)
    expect(wrapper.findComponent({ name: 'RoundsTable' }).exists()).toBe(false)
  })
})
