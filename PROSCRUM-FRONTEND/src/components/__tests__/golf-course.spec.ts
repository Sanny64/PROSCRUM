import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { shallowMount } from "@vue/test-utils";
import GolfCourse from "../golf-course.vue";
import { createI18n } from "vue-i18n";
import i18nMessages from "../../i18n/en.json"; // i18n-Daten importieren
import type { Course } from "../../types/types";

// 🔹 i18n für Tests
const i18n = createI18n({
  legacy: false,
  locale: "en",
  messages: { en: i18nMessages },
});

// 🔹 Mock-Daten für Course
const mockCourse: Course = {
  course_name: "Sunny Hills Golf Course",
  course_par: 72,
  course_rating_9: null,
  course_rating_18: 70.9,
  slope_rating: 115,
  holes: [
    { hole: 1, par: 3, hdc: 4 },
    { hole: 2, par: 4, hdc: 16 },
    { hole: 3, par: 4, hdc: 1 },
  ],
  course_id: 1,
};

describe("GolfCourse.vue", () => {
  let wrapper: ReturnType<typeof shallowMount>;

  beforeEach(() => {
    vi.clearAllMocks();
    wrapper = shallowMount(GolfCourse, {
      global: { plugins: [i18n] },
      props: { course: mockCourse },
    });
  });

  afterEach(() => {
    wrapper.unmount();
  });

  // ✅ Test: Komponente sollte ohne Fehler gerendert werden
  it("should render the GolfCourse component", () => {
    expect(wrapper.exists()).toBe(true);
  });

  // ✅ Test: Grid-View wird initial angezeigt
  it("should display the grid view initially", () => {
    expect(wrapper.find(".gridView").exists()).toBe(true);
    expect(wrapper.find(".inputView").exists()).toBe(false);
  });

  // ✅ Test: Beim Klicken auf die gridView wird die Detailansicht geöffnet
  it("should open the details view when gridView is clicked", async () => {
    await wrapper.find(".gridView").trigger("click");
    expect(wrapper.find(".inputView").exists()).toBe(true);
    expect(wrapper.find(".gridView").exists()).toBe(false);
  });

  // ✅ Test: Kursdetails werden in der Detailansicht korrekt angezeigt
  it("should display course details in the details view", async () => {
    await wrapper.find(".gridView").trigger("click");

    expect(wrapper.find(".formView").exists()).toBe(true);
    expect(wrapper.find(".formView").text()).toContain("Sunny Hills Golf Course");
    expect(wrapper.find(".formView").text()).toContain("72");     // Par
    expect(wrapper.find(".formView").text()).toContain("70.9");   // Course Rating
    expect(wrapper.find(".formView").text()).toContain("115");    // Slope Rating
  });

  // ✅ Test: Löcher werden korrekt angezeigt
  it("should display holes correctly", async () => {
    await wrapper.find(".gridView").trigger("click");
    const holes = wrapper.findAll(".hole");
    expect(holes.length).toBe(3); // Drei Löcher im Mock-Daten

    expect(holes[0].text()).toContain("1."); // Hole 1
    expect(holes[0].text()).toContain("3");  // Par
    expect(holes[0].text()).toContain("4");  // HDC

    expect(holes[1].text()).toContain("2.");
    expect(holes[1].text()).toContain("4");
    expect(holes[1].text()).toContain("16");

    expect(holes[2].text()).toContain("3.");
    expect(holes[2].text()).toContain("4");
    expect(holes[2].text()).toContain("1");
  });

  // ✅ Test: Button zum Schließen der Detailansicht funktioniert
  it("should close the details view when the close button is clicked", async () => {
    await wrapper.find(".gridView").trigger("click");
    expect(wrapper.find(".inputView").exists()).toBe(true);

    await wrapper.findAll(".submit-btn").at(1)?.trigger("click"); // Close-Button
    expect(wrapper.find(".gridView").exists()).toBe(true);
    expect(wrapper.find(".inputView").exists()).toBe(false);
  });

  // ✅ Test: Klick auf den Delete-Button emittiert "course-deleted" Event
  it('should emit "course-deleted" event when the delete button is clicked', async () => {
    await wrapper.find(".gridView").trigger("click");

    const deleteButton = wrapper.findAll(".submit-btn").at(0); // Delete-Button
    await deleteButton?.trigger("click");

    expect(wrapper.emitted("course-deleted")).toBeTruthy();
    expect(wrapper.emitted("course-deleted")?.[0]).toEqual([mockCourse]);
  });

  // ✅ Test: Kursbild wird mit dem richtigen Pfad angezeigt
  it("should display the course icon with the correct path", () => {
    const img = wrapper.find(".gridViewImage img");
    expect(img.exists()).toBe(true);
    expect(img.attributes("src")).toContain("/assets/courseIcons/2.png"); // course_id = 1 → (1 % 10 + 1) = 2
  });
});
