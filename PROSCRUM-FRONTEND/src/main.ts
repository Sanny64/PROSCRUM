import './style/main.css'

import { createApp} from 'vue'
import App from './App.vue'
import router from './router'
import { createI18n, type Composer } from 'vue-i18n'

import de from './i18n/de.json'
import en from './i18n/en.json'
import hs from './i18n/hs.json'

type Schema = typeof de

 const i18n = createI18n<[Schema], 'en' | 'de' | 'hs'>({
   legacy: false, locale: 'de', // Standard-Sprache
  fallbackLocale: 'en', // Falls eine Übersetzung fehlt
  messages: { en, de, hs },
})

const app = createApp(App)
app.use(i18n)
app.use(router)

app.mount('#app')

export { i18n };
