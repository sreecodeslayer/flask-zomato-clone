import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Login from './views/Login.vue'

Vue.use(Router)

let router = new Router({
  mode: 'history',
  // base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { public: true }
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('./views/About.vue')
    }
  ]
})

// goto login page if user is not autheroized
router.beforeEach(function (to, from, next) {
  if (!to.meta.public && !router.app.$auth.isAuthenticated()) {
    next('/login')
  } else {
    next()
  }
})

export default router
