import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { shallowMount } from "@vue/test-utils";
import RoundsTable from "../rounds-table.vue";
import { createI18n } from "vue-i18n";
import type { Round } from "../../types/types";

// 🔹 i18n für Tests mit englischer Übersetzung
export const i18n = createI18n({
  legacy: false,
  locale: "en",
  messages: {
    en: {
      output: {
        round: "Round",
        resultsFrom2021: "Results from 2021",
        resultsUntil2020: "Results until 2020",
        scoreDifferential: "Score Differential",
        more: "More",
        fewer: "Fewer",
      },
    },
  },
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

describe("RoundsTable.vue", () => {
  let wrapper: ReturnType<typeof shallowMount>;

  beforeEach(() => {
    vi.clearAllMocks();
    wrapper = shallowMount(RoundsTable, {
      global: { plugins: [i18n] },
      props: { roundsData: mockRoundsData },
    });
  });

  afterEach(() => {
    wrapper.unmount();
  });

  // ✅ Test: Die Komponente sollte ohne Fehler gerendert werden
  it("should render the RoundsTable component", () => {
    expect(wrapper.exists()).toBe(true);
  });

  // ✅ Test: Tabelle wird korrekt gerendert
  it("should render a table with the correct headers", () => {
    const headers = wrapper.findAll("th");
    expect(headers.length).toBe(4);
    expect(headers[0].text()).toBe("Round");
    expect(headers[1].text()).toBe("Results from 2021");
    expect(headers[2].text()).toBe("Results until 2020");
    expect(headers[3].text()).toBe("Score Differential");
  });

  // ✅ Test: Standardmäßig sollten maximal 5 Zeilen sichtbar sein
  it("should show a maximum of 5 rounds initially", () => {
    const rows = wrapper.findAll("tbody tr:not(.more-row)");
    expect(rows.length).toBe(5);
  });

  // ✅ Test: "Mehr"-Button sollte erscheinen, wenn es mehr als 5 Einträge gibt
  it('should display "More" button when there are more rounds', () => {
    const moreButton = wrapper.find(".more-row");
    expect(moreButton.exists()).toBe(true);
    expect(moreButton.text()).toBe("More");
  });

  // ✅ Test: Klicken auf "Mehr" zeigt alle Runden an
  it('should display all rounds when clicking "More" button', async () => {
    await wrapper.find(".more-row").trigger("click");
    const rows = wrapper.findAll("tbody tr:not(.more-row)");
    expect(rows.length).toBe(mockRoundsData.length);
  });

  // ✅ Test: "Weniger"-Button erscheint nach Klick auf "Mehr"
  it('should display "Fewer" button after clicking "More"', async () => {
    await wrapper.find(".more-row").trigger("click");
    const fewerButton = wrapper.find(".more-row");
    expect(fewerButton.exists()).toBe(true);
    expect(fewerButton.text()).toBe("Fewer");
  });

  // ✅ Test: Klicken auf "Weniger" reduziert die Anzahl der sichtbaren Zeilen wieder auf 5
  it('should hide extra rounds when clicking "Fewer" button', async () => {
    await wrapper.find(".more-row").trigger("click"); // Zeigt alle Zeilen
    await wrapper.find(".more-row").trigger("click"); // Klickt auf "Fewer"

    const rows = wrapper.findAll("tbody tr:not(.more-row)");
    expect(rows.length).toBe(5);
  });
});
