import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { shallowMount } from "@vue/test-utils";
import { nextTick } from "vue";
import CourseFilter from "../course-filter.vue";
import { createI18n } from "vue-i18n";
import type { Course } from "../../types/types";

// 🔹 i18n für Tests mit englischer Übersetzung
export const i18n = createI18n({
  legacy: false,
  locale: "en",
  messages: {
    en: {
      filter: {
        search: "Search...",
        maxCourseRating: "Max. Course Rating: ",
        maxSlopeRating: "Max. Slope Rating: ",
      },
    },
  },
});

// 🔹 Mock-Daten für Kursliste
const mockCourseList: Course[] = [
  {
    course_name: "Sunny Hills Golf Course",
    course_par: 72,
    course_rating_9: null,
    course_rating_18: 70.9,
    slope_rating: 115,
    holes: [],
    course_id: 1,
  },
  {
    course_name: "Shady Hills Golf Course",
    course_par: 68,
    course_rating_9: null,
    course_rating_18: 72.3,
    slope_rating: 130,
    holes: [],
    course_id: 2,
  },
];

describe("CourseFilter.vue", () => {
  let wrapper: ReturnType<typeof shallowMount>;

  beforeEach(async () => {
    vi.clearAllMocks();
    wrapper = shallowMount(CourseFilter, {
      global: { plugins: [i18n] },
      props: { courseList: [] }, // Props zunächst leer setzen
    });

    // Props nach dem Mounten setzen
    await wrapper.setProps({ courseList: mockCourseList });
  });

  afterEach(() => {
    wrapper.unmount();
  });

  // ✅ Test: Komponente sollte ohne Fehler gerendert werden
  it("should render the CourseFilter component", () => {
    expect(wrapper.exists()).toBe(true);
  });

  // ✅ Test: Suchfeld sollte gerendert werden
  it("should render the search input with correct placeholder", () => {
    const searchInput = wrapper.find(".TextInputContainer input");
    expect(searchInput.exists()).toBe(true);
    expect(searchInput.attributes("placeholder")).toBe("Search...");
  });

  // ✅ Test: Eingabe ins Suchfeld emittiert "text-value" Event
  it('should emit "text-value" event when typing in search input', async () => {
    const searchInput = wrapper.find(".TextInputContainer input");
    await searchInput.setValue("Sunny");
    expect(wrapper.emitted("text-value")).toBeTruthy();
    expect(wrapper.emitted("text-value")?.[0]).toEqual(["Sunny"]);
  });

  // ✅ Test: Max Slope Rating Slider sollte korrekt gerendert werden
  it("should render the max slope rating slider with correct max value", () => {
    const slopeSlider = wrapper.find(".maxSlopeRating input");
    expect(slopeSlider.exists()).toBe(true);
    expect(slopeSlider.attributes("max")).toBe("130"); // Höchster slope_rating im mockCourseList
  });

  // ✅ Test: Max Course Rating Slider sollte korrekt gerendert werden
  it("should render the max course rating slider with correct max value", () => {
    const courseSlider = wrapper.find(".maxCourseRating input");
    expect(courseSlider.exists()).toBe(true);
    expect(courseSlider.attributes("max")).toBe("73"); // 72.3 aufgerundet zu 73
  });

  // ✅ Test: Klicken auf Max Slope Rating Bereich aktiviert/deaktiviert den Slider
  it("should toggle slope rating slider when clicking the container", async () => {
    const slopeContainer = wrapper.find(".maxSlopeRating");
    const slopeSlider = wrapper.find(".maxSlopeRating input");

    expect(slopeSlider.attributes("disabled")).toBeUndefined();

    await slopeContainer.trigger("click");
    await nextTick();
    expect(slopeSlider.attributes("disabled")).toBeDefined();

    await slopeContainer.trigger("click");
    await nextTick();
    expect(slopeSlider.attributes("disabled")).toBeUndefined();
  });

  // ✅ Test: Klicken auf Max Course Rating Bereich aktiviert/deaktiviert den Slider
  it("should toggle course rating slider when clicking the container", async () => {
    const courseContainer = wrapper.find(".maxCourseRating");
    const courseSlider = wrapper.find(".maxCourseRating input");

    expect(courseSlider.attributes("disabled")).toBeUndefined();

    await courseContainer.trigger("click");
    await nextTick();
    expect(courseSlider.attributes("disabled")).toBeDefined();

    await courseContainer.trigger("click");
    await nextTick();
    expect(courseSlider.attributes("disabled")).toBeUndefined();
  });

  // ✅ Test: Slope Rating Änderung emittiert "slope-rating-value" Event
  it('should emit "slope-rating-value" event when slider value changes', async () => {
    const slopeSlider = wrapper.find(".maxSlopeRating input");
    await slopeSlider.setValue('100');
    expect(wrapper.emitted("slope-rating-value")).toBeTruthy();
    expect(wrapper.emitted("slope-rating-value")?.[0][0]).toEqual('100');


  });

  // ✅ Test: Course Rating Änderung emittiert "course-rating-value" Event
  it('should emit "course-rating-value" event when slider value changes', async () => {
    const courseSlider = wrapper.find(".maxCourseRating input");
    await courseSlider.setValue("70");
    expect(wrapper.emitted("course-rating-value")).toBeTruthy();
    expect(wrapper.emitted("course-rating-value")?.[0][0]).toEqual("70");
  });
});
