import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { shallowMount } from "@vue/test-utils";
import CalculationInput from "../calculation-input.vue";
import { createI18n } from "vue-i18n";
import { nextTick } from "vue";
import type { Course } from "../../types/types";

// 🔹 i18n für Tests mit englischer Übersetzung
export const i18n = createI18n({
  legacy: false,
  locale: "en",
  messages: {
    en: {
      "input": {
        input: "Input",
        round: "Round: ",
        courseRating: "Course Rating: ",
        slopeRating: "Slope Rating: ",
        courseSelection: "Select a course",
        holes: "Holes",
        hole: ". Hole: ",
        calculate: "Calculate"
      },
    }
  }
});

// 🔹 Mock-Daten für Kursliste
const mockCourseList: Course[] =[
  {
    "course_name":"Sunny Hills Golf Course",
    "course_par":72,
    "course_rating_9":null,
    "course_rating_18":70.9,
    "slope_rating":115,
    "holes":[
      {
        "hole":1,
        "par":3,
        "hdc":4
      },
      {
        "hole":2,
        "par":4,
        "hdc":16
      },
      {
        "hole":3,
        "par":4,
        "hdc":1
      },
      {
        "hole":4,
        "par":5,
        "hdc":10
      },
      {
        "hole":5,
        "par":4,
        "hdc":7
      },
      {
        "hole":6,
        "par":4,
        "hdc":13
      },
      {
        "hole":7,
        "par":3,
        "hdc":5
      },
      {
        "hole":8,
        "par":4,
        "hdc":17
      },
      {
        "hole":9,
        "par":4,
        "hdc":2
      },
      {
        "hole":10,
        "par":5,
        "hdc":11
      },
      {
        "hole":11,
        "par":4,
        "hdc":8
      },
      {
        "hole":12,
        "par":4,
        "hdc":14
      },
      {
        "hole":13,
        "par":3,
        "hdc":6
      },
      {
        "hole":14,
        "par":4,
        "hdc":18
      },
      {
        "hole":15,
        "par":4,
        "hdc":3
      },
      {
        "hole":16,
        "par":5,
        "hdc":12
      },
      {
        "hole":17,
        "par":4,
        "hdc":9
      },
      {
        "hole":18,
        "par":4,
        "hdc":15
      }
    ],
    "course_id":1
  },
  {
    "course_name":"Shady Hills Golf Course",
    "course_par":68,
    "course_rating_9":null,
    "course_rating_18":72.3,
    "slope_rating":130,
    "holes":[
      {
        "hole":1,
        "par":3,
        "hdc":16
      },
      {
        "hole":2,
        "par":4,
        "hdc":1
      },
      {
        "hole":3,
        "par":4,
        "hdc":10
      },
      {
        "hole":4,
        "par":5,
        "hdc":7
      },
      {
        "hole":5,
        "par":4,
        "hdc":13
      },
      {
        "hole":6,
        "par":4,
        "hdc":4
      },
      {
        "hole":7,
        "par":3,
        "hdc":17
      },
      {
        "hole":8,
        "par":4,
        "hdc":2
      },
      {
        "hole":9,
        "par":4,
        "hdc":11
      },
      {
        "hole":10,
        "par":5,
        "hdc":8
      },
      {
        "hole":11,
        "par":4,
        "hdc":14
      },
      {
        "hole":12,
        "par":4,
        "hdc":5
      },
      {
        "hole":13,
        "par":3,
        "hdc":18
      },
      {
        "hole":14,
        "par":4,
        "hdc":3
      },
      {
        "hole":15,
        "par":4,
        "hdc":12
      },
      {
        "hole":16,
        "par":5,
        "hdc":9
      },
      {
        "hole":17,
        "par":4,
        "hdc":15
      },
      {
        "hole":18,
        "par":4,
        "hdc":6
      }
    ],
    "course_id":2
  },
  {
    "course_name":"Cedar Ridge Golf Course",
    "course_par":35,
    "course_rating_9":34.1,
    "course_rating_18":74.1,
    "slope_rating":115,
    "holes":[
      {
        "hole":1,
        "par":3,
        "hdc":4
      },
      {
        "hole":2,
        "par":4,
        "hdc":16
      },
      {
        "hole":3,
        "par":4,
        "hdc":1
      },
      {
        "hole":4,
        "par":5,
        "hdc":10
      },
      {
        "hole":5,
        "par":4,
        "hdc":7
      },
      {
        "hole":6,
        "par":4,
        "hdc":13
      },
      {
        "hole":7,
        "par":3,
        "hdc":5
      },
      {
        "hole":8,
        "par":4,
        "hdc":17
      },
      {
        "hole":9,
        "par":4,
        "hdc":2
      }
    ],
    "course_id":3
  },
  {
    "course_name":"Sunny Hills Golf Course",
    "course_par":35,
    "course_rating_9":35.7,
    "course_rating_18":70.1,
    "slope_rating":130,
    "holes":[
      {
        "hole":1,
        "par":3,
        "hdc":4
      },
      {
        "hole":2,
        "par":4,
        "hdc":16
      },
      {
        "hole":3,
        "par":4,
        "hdc":1
      },
      {
        "hole":4,
        "par":5,
        "hdc":10
      },
      {
        "hole":5,
        "par":4,
        "hdc":7
      },
      {
        "hole":6,
        "par":4,
        "hdc":13
      },
      {
        "hole":7,
        "par":3,
        "hdc":5
      },
      {
        "hole":8,
        "par":4,
        "hdc":17
      },
      {
        "hole":9,
        "par":4,
        "hdc":2
      }
    ],
    "course_id":4
  }
];

describe("CalculationInput.vue", () => {
  let wrapper: ReturnType<typeof shallowMount>;

  beforeEach(() => {
    vi.clearAllMocks();
    wrapper = shallowMount(CalculationInput, {
      global: { plugins: [i18n] },
      props: { courseList: mockCourseList }
    });
  });

  afterEach(() => {
    wrapper.unmount();
  });

  // ✅ Test: Die Komponente sollte ohne Fehler gerendert werden
  it("should render the CalculationInput component", () => {
    expect(wrapper.exists()).toBe(true);
  });

  // ✅ Test: Das Dropdown-Menü öffnet sich beim Klicken
  it("should toggle dropdown visibility", async () => {
    expect(wrapper.find(".dropdown-menu").exists()).toBe(false);

    await wrapper.find(".dropdown-button").trigger("click");
    await nextTick();

    expect(wrapper.find(".dropdown-menu").exists()).toBe(true);

    await wrapper.find(".dropdown-button").trigger("click");
    await nextTick();

    expect(wrapper.find(".dropdown-menu").exists()).toBe(false);
  });

  // ✅ Test: Eine Auswahl setzt den richtigen Kurs
  it("should select a course from the dropdown", async () => {
    await wrapper.find(".dropdown-button").trigger("click");
    await nextTick();

    const firstCourseItem = wrapper.findAll(".dropdown-item").at(0);
    await firstCourseItem?.trigger("click");
    await nextTick();

    expect(wrapper.find(".dropdown-button").text()).toBe("Sunny Hills Golf Course");
  });




  // ✅ Test: Beim Absenden wird das `formData`-Event mit den korrekten Daten emittiert
  it("should emit formData event on submit", async () => {
    await wrapper.find(".dropdown-button").trigger("click");
    await nextTick();

    const firstCourseItem = wrapper.findAll(".dropdown-item").at(0);
    await firstCourseItem?.trigger("click");
    await nextTick();

    await wrapper.find("form").trigger("submit.prevent");
    await nextTick();

    expect(wrapper.emitted("formData")).toBeTruthy();
    expect(wrapper.emitted("formData")?.[0][0]).toMatchObject({
      round_number: undefined,
      course: mockCourseList[0],
      scores: expect.any(Array),
    });
  });
});
