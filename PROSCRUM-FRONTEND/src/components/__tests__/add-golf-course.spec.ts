import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { shallowMount } from "@vue/test-utils";
import AddGolfCourse from "../add-golf-course.vue";
import { createI18n } from "vue-i18n";
import { nextTick } from "vue";

export const i18n = createI18n({
  legacy: false,
  locale: "en",
  messages: {
    en: {
      coursePage: {
        courseName: "Course name: ",
        par: "Par: ",
        courseRating: "Course Rating: ",
        slopeRating: "Slope Rating: ",
        hole: "Hole: ",
        hdc: "HDC.: ",
        save: "Save",
        delete: "Delete",
        close: "Close"
      },
    }
  }
});

describe("AddGolfCourse.vue", () => {
  let wrapper: ReturnType<typeof shallowMount>;

  beforeEach(() => {
    vi.clearAllMocks();
    wrapper = shallowMount(AddGolfCourse, {
      global: { plugins: [i18n] }
    });
  });

  afterEach(() => {
    wrapper.unmount();
  });

  // ✅ Test: Die Komponente sollte ohne Fehler gerendert werden
  it("should render the AddGolfCourse component", () => {
    expect(wrapper.exists()).toBe(true);
  });

  // ✅ Test: Standardmäßig wird das `gridView` angezeigt
  it("should display gridView by default", () => {
    expect(wrapper.find(".gridView").exists()).toBe(true);
    expect(wrapper.find(".inputView").exists()).toBe(false);
  });

  // ✅ Test: Beim Klicken auf das `gridView` wird das Formular (`inputView`) angezeigt
  it("should show inputView when clicking gridView", async () => {
    await wrapper.find(".gridView").trigger("click");
    await nextTick();

    expect(wrapper.find(".gridView").exists()).toBe(false);
    expect(wrapper.find(".inputView").exists()).toBe(true);
  });

  // ✅ Test: Das Formular enthält die erwarteten Eingabefelder
  it("should render form fields correctly", async () => {
    await wrapper.find(".gridView").trigger("click");
    await nextTick();

    expect(wrapper.find("input#course_name").exists()).toBe(true);
    expect(wrapper.find("input#courseRating").exists()).toBe(true);
    expect(wrapper.find("input#slopeRating").exists()).toBe(true);
  });

  // ✅ Test: Beim Absenden wird das `course-added`-Event mit den korrekten Daten emittiert
  it("should emit course-added event on form submit", async () => {
    await wrapper.find(".gridView").trigger("click");
    await nextTick();

    await wrapper.find("form").trigger("submit.prevent");
    await nextTick();

    expect(wrapper.emitted("course-added")).toBeTruthy();
    expect(wrapper.emitted("course-added")?.[0][0]).toEqual(expect.objectContaining({
      course_name: "Platz 3 - Windige Wiese",
      course_par: expect.any(Number),
      course_rating_18: 74,
      slope_rating: 128
    }));
  });

  // ✅ Test: Beim Klicken auf "Close" wird das `gridView` wieder angezeigt
  it("should close the form and show gridView on close", async () => {
    await wrapper.find(".gridView").trigger("click");
    await nextTick();

    await wrapper.find("button[type='button']").trigger("click");
    await nextTick();

    expect(wrapper.find(".gridView").exists()).toBe(true);
    expect(wrapper.find(".inputView").exists()).toBe(false);
  });

  // ✅ Test: Änderungen an den Par-Werten aktualisieren `course_par`
  it("should update course_par when hole par values change", async () => {
    await wrapper.find(".gridView").trigger("click");
    await nextTick();

    const holeInput = wrapper.find("input[id='hole-1']");
    await holeInput.setValue("5");
    await nextTick();

    const courseParValue = wrapper.find("b").text();
    expect(Number(courseParValue)).toBeGreaterThan(72); // Sollte sich aktualisiert haben
  });
});
