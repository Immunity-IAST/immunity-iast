//import './assets/main.css'
import 'uikit/dist/css/uikit.min.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import UIkit from 'uikit'
import Icons from 'uikit/dist/js/uikit-icons'

UIkit.use(Icons)

const app = createApp(App)

app.config.globalProperties.$UIkit = UIkit

app.use(createPinia())
app.use(router)

app.mount('#app')
