import { createRouter, createWebHistory } from 'vue-router'
import { useCurrentIndexStore } from '@/stores/currentIndex'
import HomeView from '../views/HomeView.vue'
import EventView from '@/views/EventView.vue'
import AboutView from '@/views/AboutView.vue'

const routeData = [
  {
    route: "/",
    routeName: "home",
    buttonSubtitle: "首页",
    buttonTitle: "Home page",
    component: HomeView
  },
  {
    route: "/about",
    routeName: "about",
    buttonSubtitle: "关于",
    buttonTitle: "About",
    component: AboutView
  },
  {
    route: "/events",
    routeName: "events",
    buttonSubtitle: "活动",
    buttonTitle: "Events",
    component: EventView
  }
]

const routerList = routeData.map(
  (value) => ({
    path: value.route,
    name: value.routeName,
    component: value.component
  })
)

export const routeButtonData = routeData.map(
  (value) => ({
    title: value.buttonTitle,
    subtitle: value.buttonSubtitle,
    path: value.route
  })
)

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routerList
})

router.afterEach((to, from) => {
  const toIndex = routeData.findIndex((value) => {
    if (value.route === to.path) return true
    return false
  })
  const fromIndex = routeData.findIndex((value) => {
    if (value.route === from.path) return true
    return false
  })
  const { setIndex } = useCurrentIndexStore()
  setIndex(toIndex)
  to.meta.transition = toIndex >= fromIndex ? 'forward' : 'rewind'
})

export default router
