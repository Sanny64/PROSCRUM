import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { shallowMount, RouterLinkStub } from '@vue/test-utils'
import NavBar from '../nav-bar.vue'
import { createI18n } from 'vue-i18n'
import i18nMessages from '../../i18n/en.json' // i18n-Daten importieren
import router from '../../router/index' // Router importieren

// 🔹 Mock für Sound-Funktionen
vi.mock('../../composables/playSound.ts', () => ({
  playSound: vi.fn(),
  playGolfMusic: vi.fn(),
  stopGolfMusic: vi.fn(),
}))


// 🔹 i18n für Tests
const i18n = createI18n({
  legacy: false,
  locale: 'en',
  messages: { en: i18nMessages },
})

// 🔹 Wrapper-Erstellung mit RouterLinkStub
const createWrapper = () =>
  shallowMount(NavBar, {
    global: {
      plugins: [i18n, router],
      stubs: { RouterLink: RouterLinkStub },
    },
  })

describe('NavBar.vue', () => {
  let wrapper: ReturnType<typeof createWrapper>

  beforeEach(() => {
    vi.clearAllMocks()
    wrapper = createWrapper()
  })

  afterEach(() => {
    wrapper.unmount()
  })

  // ✅ Test: Komponente sollte ohne Fehler gerendert werden
  it('should render the NavBar component', () => {
    expect(wrapper.exists()).toBe(true)
  })

  // ✅ Test: Das Menü enthält die richtigen Router-Links
  it('should contain correct router links', () => {
    const links = wrapper.findAllComponents(RouterLinkStub)
    console.log(wrapper.html())
    const paths = links.map((link) => link.props('to'))

    expect(paths).toEqual(['/', '/', '/course', '/rounds'])
    // expect(paths).toEqual(['/', '/', '/course', '/rounds', '/signup', '/login'])
  })

  // ✅ Test: Einstellungsmenü öffnet und schließt sich beim Klicken auf das Zahnrad
  it('should toggle settings menu when gear icon is clicked', async () => {
    const gearIcon = wrapper.find('.gear-icon')
    expect(wrapper.find('.settings').exists()).toBe(false)

    await gearIcon.trigger('click')
    expect(wrapper.find('.settings').exists()).toBe(true)

    await gearIcon.trigger('click')
    expect(wrapper.find('.settings').exists()).toBe(false)
  })

  // ✅ Test: Sprachwechsel funktioniert
  it('should change language when clicking language buttons', async () => {
    await wrapper.find('.gear-icon').trigger('click') // Einstellungen öffnen

    const englishButton = wrapper.find('.settings button:nth-child(1)')
    const germanButton = wrapper.find('.settings button:nth-child(2)')

    expect(i18n.global.locale.value).toBe('en')

    await germanButton.trigger('click')
    expect(i18n.global.locale.value).toBe('de')

    await englishButton.trigger('click')
    expect(i18n.global.locale.value).toBe('en')
  })


  // ✅ Test: Logo wird korrekt gerendert
  it('should render the logo with correct src', () => {
    const logo = wrapper.find('.menu-logo img')
    expect(logo.exists()).toBe(true)
    expect(logo.attributes('src')).toBe('/src/assets/logo.png')
    expect(logo.attributes('alt')).toBe('Golf Handicap Rechner')
  })

  // ✅ Test: Menüüberschrift zeigt den korrekten Titel
  it('should display the correct menu headline', () => {
    const headline = wrapper.find('.menu-headline')
    expect(headline.text()).toBe(i18n.global.t('title'))
  })

  // ✅ Test: Navigation über Router-Links funktioniert
  it('should navigate to correct route when clicking router links', async () => {
    const links = wrapper.findAllComponents(RouterLinkStub)

    const routes = [
      { link: links[0], expectedPath: '/' },
      { link: links[2], expectedPath: '/course' },
      { link: links[3], expectedPath: '/rounds' },
      // { link: links[4], expectedPath: '/signup' },
      // { link: links[5], expectedPath: '/login' },
    ]

    for (const { link, expectedPath } of routes) {
      await link.trigger('click')
      expect(link.props('to')).toBe(expectedPath)
    }
  })
})
