import Vue from "vue";
import VueRouter from "vue-router";
import Login from "../views/Login.vue";
import Home from "../views/Home.vue";
import Trip from "../views/Trip.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Login",
    component: Login,
    meta: {
      hideNavigationBar: true
    }
  },
  {
    path: "/home",
    name: "Home",
    component: Home,
    meta: {
      hideNavigationBar: false
    }
  },
  {
    path: "/trip",
    name: "Trip",
    component: Trip,
    meta: {
      hideNavigationBar: false
    }
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue")
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;

