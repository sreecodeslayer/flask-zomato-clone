import Vue from 'vue'
import VueSocketIO from 'vue-socket.io'
import VueCookies from 'vue-cookies'

import router from '../router'
import io from 'socket.io-client'
Vue.use(VueCookies)
let token = window.$cookies.get('vueauth_access_token')
let sio = io(process.env.VUE_APP_SIO, { query: { token: token }, extraHeaders: { 'Authorization': 'Bearer ' + token } })

Vue.use(new VueSocketIO({
  debug: true,
  connection: sio
}))
