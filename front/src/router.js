import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Costumer from './views/Costumer.vue'
import Administrator from './views/Administrator.vue'
import Desk from './views/Desk.vue'
import Manager from './views/Manager.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/costumer',
      name: 'costumer',
      component: Costumer
    },
    {
      path: '/desk',
      name: 'desk',
      component: Desk
    },
    {
      path: '/manager',
      name: 'manager',
      component: Manager
    },
    {
      path: '/administrator',
      name: 'administrator',
      component: Administrator
    }
  ]
})
