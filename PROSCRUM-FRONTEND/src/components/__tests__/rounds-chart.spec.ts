import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { shallowMount } from "@vue/test-utils";
import RoundsChart from "../rounds-chart.vue";
import { createI18n } from "vue-i18n";
import i18nMessages from "../../i18n/en.json"; // i18n-Daten importieren
import type { Round } from "../../types/types";
import { Chart as ChartJS } from "chart.js";

// Mock für ChartJS, um Fehler in Tests zu vermeiden
vi.mock("vue-chartjs", () => ({
  Line: {
    template: "<div></div>",
  },
}));

// 🔹 i18n für Tests mit englischer Übersetzung
export const i18n = createI18n({
  legacy: false,
  locale: "en",
  messages: { en: i18nMessages },
});

// 🔹 Mock-Daten für Rundenliste
const mockRoundsData: Round[] = [
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
];

describe("RoundsChart.vue", () => {
  let wrapper: ReturnType<typeof shallowMount>;

  beforeEach(() => {
    vi.clearAllMocks();
    wrapper = shallowMount(RoundsChart, {
      global: { plugins: [i18n] },
      props: { roundsData: mockRoundsData },
    });
  });

  afterEach(() => {
    wrapper.unmount();
  });

  // ✅ Test: Die Komponente sollte ohne Fehler gerendert werden
  it("should render the RoundsChart component", () => {
    expect(wrapper.exists()).toBe(true);
  });

});
