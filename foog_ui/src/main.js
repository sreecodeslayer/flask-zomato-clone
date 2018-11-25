import Vue from 'vue'
import App from './App.vue'
import router from './router'
import VueAuthenticate from 'vue-authenticate'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueMoment from 'vue-moment'
import './plugins/element.js'
let API_ENDPOINT = process.env.VUE_APP_API
console.log(API_ENDPOINT)
axios.defaults.headers.post['Content-Type'] = 'application/json'
axios.defaults.baseURL = API_ENDPOINT
Vue.use(VueAxios, axios)

Vue.use(VueAuthenticate, {
  baseUrl: API_ENDPOINT,
  tokenName: 'access_token',
  storageType: 'cookieStorage'
})

Vue.config.productionTip = false

Vue.use(VueMoment)
Vue.filter('humanizeTime', function (value) {
  let newVal = ''
  if (typeof value === 'string') {
    newVal = value.split('+')[0]
  } else if (typeof value === 'number') {
    newVal = value
  } else {
    return 'Not available'
  }
  return Vue.moment.utc(newVal).local().fromNow()
})

Vue.filter('calendarTime', function (value) {
  let newVal = ''
  if (typeof value === 'string') {
    newVal = value.split('+')[0]
  } else if (typeof value === 'number') {
    newVal = value
  } else {
    return 'Not available'
  }
  return Vue.moment.utc(newVal).local().calendar()
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
