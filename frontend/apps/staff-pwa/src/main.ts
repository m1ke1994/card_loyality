import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import App from "./App.vue";
import "./style.css";
import Dashboard from "./pages/Dashboard.vue";
import Places from "./pages/Places.vue";
import Scan from "./pages/Scan.vue";
import UserCard from "./pages/UserCard.vue";
import Checkout from "./pages/Checkout.vue";

const routes = [
  { path: "/staff", component: Dashboard },
  { path: "/staff/places", component: Places },
  { path: "/staff/scan", component: Scan },
  { path: "/staff/user/:id", component: UserCard },
  { path: "/staff/checkout/:visit_id", component: Checkout }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

createApp(App).use(router).mount("#app");
