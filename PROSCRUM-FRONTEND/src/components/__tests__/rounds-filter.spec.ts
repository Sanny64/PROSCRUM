import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { shallowMount } from "@vue/test-utils";
import { nextTick } from "vue";
import RoundsFilter from "../rounds-filter.vue";
import { createI18n } from "vue-i18n";
import type { Round } from "../../types/types";
import i18nMessages from "../../i18n/en.json"; // i18n-Daten importieren


// 🔹 i18n für Tests mit englischer Übersetzung
export const i18n = createI18n({
  legacy: false,
  locale: "en",
  messages: { en: i18nMessages },
});

// 🔹 Mock-Daten für Rundenliste
const mockRoundsList: Round[] = [
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

describe("RoundsFilter.vue", () => {
  let wrapper: ReturnType<typeof shallowMount>;

  beforeEach(async () => {
    vi.clearAllMocks();
    wrapper = shallowMount(RoundsFilter, {
      global: { plugins: [i18n] },
      props: { roundsList: [] }, // Props zunächst leer setzen
    });

    // Props nach dem Mounten setzen
    await wrapper.setProps({ roundsList: mockRoundsList });
  });

  afterEach(() => {
    wrapper.unmount();
  });

  // ✅ Test: Komponente sollte ohne Fehler gerendert werden
  it("should render the RoundsFilter component", () => {
    expect(wrapper.exists()).toBe(true);
  });

  // ✅ Test: Suchfeld sollte gerendert werden
  it("should render the search input with correct placeholder", () => {
    const searchInput = wrapper.find(".TextInputContainer input");
    expect(searchInput.exists()).toBe(true);
    expect(searchInput.attributes("placeholder")).toBe("Search...");
  });

  // ✅ Test: Eingabe ins Suchfeld emittiert "text-value" Event
  it("should emit 'text-value' event when typing in search input", async () => {
    const searchInput = wrapper.find(".TextInputContainer input");
    await searchInput.setValue("Sunny");
    expect(wrapper.emitted("text-value")).toBeTruthy();
    expect(wrapper.emitted("text-value")?.[0]).toEqual(["Sunny"]);
  });

  // ✅ Test: Zahlenfeld sollte gerendert werden
  it("should render the number input with correct placeholder", () => {
    const numberInput = wrapper.find(".NumberInputContainer input");
    expect(numberInput.exists()).toBe(true);
    expect(numberInput.attributes("placeholder")).toBe("Number");
  });

  // ✅ Test: Eingabe in das Zahlenfeld emittiert "number-value" Event
  it("should emit 'number-value' event when typing in number input", async () => {
    const numberInput = wrapper.find(".NumberInputContainer input");
    await numberInput.setValue("2");
    expect(wrapper.emitted("number-value")).toBeTruthy();
    expect(wrapper.emitted("number-value")?.[0]).toEqual([2]);
  });

});
