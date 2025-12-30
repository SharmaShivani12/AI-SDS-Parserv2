import { createApp } from 'vue'

import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

import Home from './pages/Home.vue'
import SDSList from './pages/SDSList.vue'
import SDSDetail from './pages/SDSDetail.vue'
import './style.css'

const routes = [
    { path: '/', component: Home },
    { path: '/sds', component: SDSList },
    { path: '/sds/:id', component: SDSDetail, props: true },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

createApp(App).use(router).mount('#app')

