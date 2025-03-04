import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { shallowMount } from "@vue/test-utils";
import GolfRound from "../golf-round.vue";
import { createI18n } from "vue-i18n";
import i18nMessages from "../../i18n/en.json"; // i18n-Daten importieren

// 🔹 i18n für Tests
const i18n = createI18n({
  legacy: false,
  locale: "en",
  messages: { en: i18nMessages },
});

// 🔹 Mock-Daten für eine Runde
const mockRound = {
  round_number: 1,
  course: {
    course_name: "Sunny Hills Golf Course",
    course_par: 72,
    course_rating_18: 70.9,
    slope_rating: 115,
    holes: [
      { hole: 1, par: 3, hdc: 4 },
      { hole: 2, par: 4, hdc: 16 },
      { hole: 3, par: 4, hdc: 1 },
    ],
  },
  scores: [3, 5, 4], // Score für jedes Loch
};

describe("GolfRound.vue", () => {
  let wrapper: ReturnType<typeof shallowMount>;

  beforeEach(() => {
    vi.clearAllMocks();
    wrapper = shallowMount(GolfRound, {
      global: { plugins: [i18n] },
      props: { rounds: mockRound },
    });
  });

  afterEach(() => {
    wrapper.unmount();
  });

  // ✅ Test: Komponente sollte ohne Fehler gerendert werden
  it("should render the GolfRound component", () => {
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

  // ✅ Test: Rundendetails werden in der Detailansicht korrekt angezeigt
  it("should display round details in the details view", async () => {
    await wrapper.find(".gridView").trigger("click");

    expect(wrapper.find(".formView").exists()).toBe(true);
    expect(wrapper.find(".formView").text()).toContain("Sunny Hills Golf Course");
    expect(wrapper.find(".formView").text()).toContain("1"); // Round Number
    expect(wrapper.find(".formView").text()).toContain("72"); // Par
    expect(wrapper.find(".formView").text()).toContain("70.9"); // Course Rating
    expect(wrapper.find(".formView").text()).toContain("115"); // Slope Rating
  });

  // ✅ Test: Löcher werden korrekt angezeigt
  it("should display holes correctly", async () => {
    await wrapper.find(".gridView").trigger("click");
    const holes = wrapper.findAll(".hole");
    expect(holes.length).toBe(3); // Drei Löcher im Mock-Daten

    expect(holes[0].text()).toContain("1."); // Hole 1
    expect(holes[0].text()).toContain("3"); // Par
    expect(holes[0].text()).toContain("4"); // HDC
    expect(holes[0].text()).toContain("3"); // Score

    expect(holes[1].text()).toContain("2.");
    expect(holes[1].text()).toContain("4");
    expect(holes[1].text()).toContain("16");
    expect(holes[1].text()).toContain("5");

    expect(holes[2].text()).toContain("3.");
    expect(holes[2].text()).toContain("4");
    expect(holes[2].text()).toContain("1");
    expect(holes[2].text()).toContain("4");
  });

  // ✅ Test: Button zum Schließen der Detailansicht funktioniert
  it("should close the details view when the close button is clicked", async () => {
    await wrapper.find(".gridView").trigger("click");
    expect(wrapper.find(".inputView").exists()).toBe(true);

    await wrapper.findAll(".submit-btn").at(1)?.trigger("click"); // Close-Button
    expect(wrapper.find(".gridView").exists()).toBe(true);
    expect(wrapper.find(".inputView").exists()).toBe(false);
  });

  // ✅ Test: Klick auf den Update-Button öffnet den Bearbeitungsmodus
  it("should open the edit mode when the update button is clicked", async () => {
    await wrapper.find(".gridView").trigger("click");
    await wrapper.findAll(".submit-btn").at(0)?.trigger("click"); // Update-Button
    expect(wrapper.find("form").exists()).toBe(true);
  });



  // ✅ Test: Beim Absenden wird das `updated-round`-Event mit den korrekten Daten emittiert
  it("should emit updated-round event on submit", async () => {
    await wrapper.find(".gridView").trigger("click");
    await wrapper.findAll(".submit-btn").at(0)?.trigger("click"); // Update-Button

    await wrapper.find("form").trigger("submit.prevent");

    expect(wrapper.emitted("updated-round")).toBeTruthy();
    expect(wrapper.emitted("updated-round")?.[0][0]).toEqual(mockRound);
  });

  // ✅ Test: Zurück-Button im Bearbeitungsmodus schaltet zurück zur Detailansicht
  it("should return to details view when back button is clicked in edit mode", async () => {
    await wrapper.find(".gridView").trigger("click");
    await wrapper.findAll(".submit-btn").at(0)?.trigger("click"); // Update-Button
    expect(wrapper.find("form").exists()).toBe(true);

    await wrapper.findAll(".submit-btn").at(1)?.trigger("click"); // Back-Button
    expect(wrapper.find("form").exists()).toBe(false);
    expect(wrapper.find(".inputView").exists()).toBe(true);
  });
});
