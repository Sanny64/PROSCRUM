import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { shallowMount } from "@vue/test-utils";
import RoundsPage from "../RoundsPage.vue";
import { createI18n } from "vue-i18n";
import i18nMessages from '../../i18n/en.json' // i18n-Daten importieren
import { ref, nextTick } from "vue";

// 🔹 Mock-Funktionen für API-Aufrufe
const getRoundsAPIMock = vi.fn();
const updateRoundAPIMock = vi.fn();

// 🔹 Mock für `apiCallRounds`
const apiResultRounds = ref([]); // Leere Rundenliste als Startwert

vi.mock("@/composables/api-call-rounds.ts", () => ({
  apiCallRounds: vi.fn(() => ({
    apiResultRounds, // Leere Liste als Startwert
    getRoundsAPI: getRoundsAPIMock,
    updateRoundAPI: updateRoundAPIMock,
  })),
}));

import { apiCallRounds } from "@/composables/api-call-rounds";

// 🔹 Mock für `apiCallInlineResponse`
const apiStatus = ref(200);
const sendFormdataMock = vi.fn();

vi.mock("@/composables/api-call-inline-response.ts", () => ({
  apiCallInlineResponse: vi.fn(() => ({
    apiStatus,
    sendFormdata: sendFormdataMock,
  })),
}));

import { apiCallInlineResponse } from "@/composables/api-call-inline-response";

// 🔹 i18n für Tests mit englischer Übersetzung
export const i18n = createI18n({
  legacy: false,
  locale: 'en',
  messages: { en: i18nMessages },
})

describe("RoundsPage.vue", () => {
  let wrapper: ReturnType<typeof shallowMount>;

  beforeEach(() => {
    vi.clearAllMocks();
    wrapper = shallowMount(RoundsPage, {
      global: { plugins: [i18n] },
    });
  });

  afterEach(() => {
    wrapper.unmount();
  });

  // ✅ Test: Die Komponente sollte ohne Fehler gerendert werden
  it("should render the RoundsPage component", () => {
    expect(wrapper.exists()).toBe(true);
  });

  // ✅ Test: RoundsFilter wird korrekt gerendert
  it("should render RoundsFilter component", () => {
    const filterComponent = wrapper.findComponent({ name: "RoundsFilter" });
    expect(filterComponent.exists()).toBe(true);
  });

  // ✅ Test: CalculationOutput wird korrekt gerendert
  it("should render CalculationOutput component", () => {
    const calculationComponent = wrapper.findComponent({ name: "CalculationOutput" });
    expect(calculationComponent.exists()).toBe(true);
    expect(calculationComponent.props("pollingStatus")).toBe(apiStatus.value);
    expect(calculationComponent.props("roundsResult")).toEqual([]);
  });

  // ✅ Test: GolfRound-Komponenten werden für gefilterte Runden gerendert
  it("should render GolfRound components for filteredRoundsList", async () => {
    const { apiResultRounds } = apiCallRounds();

    apiResultRounds.value = [
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

    await nextTick();

    const roundComponents = wrapper.findAllComponents({ name: "GolfRound" });
    expect(roundComponents.length).toBe(2);
  });

  // ✅ Test: `getRoundsAPI()` wird beim Mounten aufgerufen
  it("should call getRoundsAPI on mount", () => {
    expect(getRoundsAPIMock).toHaveBeenCalled();
  });

  // ✅ Test: `updateRoundAPI()` wird aufgerufen, wenn eine Runde aktualisiert wird
  it("should call updateRoundAPI when a round is updated", async () => {
    const { apiResultRounds } = apiCallRounds();
    apiResultRounds.value = [
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

    await nextTick();

    const roundComponent = wrapper.findComponent({ name: "GolfRound" });

    roundComponent.vm.$emit("updated-round", { round_number: 1 });

    await nextTick();

    expect(updateRoundAPIMock).toHaveBeenCalledWith({ round_number: 1 });
    expect(getRoundsAPIMock).toHaveBeenCalled();
  });


});
