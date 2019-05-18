import Vue from 'vue'
import './theme/element'
import App from './App.vue'
import router from './router'
import store from './store'
import Axios from 'axios'
import VCharts from 'v-charts'
import './assets/styles/iconfont.css'

Vue.config.productionTip = false
Axios.defaults.withCredentials = true;
Vue.prototype.$ajax = Axios
Vue.use(VCharts)
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})