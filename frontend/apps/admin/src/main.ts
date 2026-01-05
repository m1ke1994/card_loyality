import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import App from "./App.vue";
import "./style.css";
import Overview from "./pages/Overview.vue";
import Places from "./pages/Places.vue";
import Staff from "./pages/Staff.vue";
import LoyaltyRules from "./pages/LoyaltyRules.vue";
import Coupons from "./pages/Coupons.vue";
import Promotions from "./pages/Promotions.vue";
import Reports from "./pages/Reports.vue";

const routes = [
  { path: "/admin", component: Overview },
  { path: "/admin/places", component: Places },
  { path: "/admin/staff", component: Staff },
  { path: "/admin/loyalty-rules", component: LoyaltyRules },
  { path: "/admin/coupons", component: Coupons },
  { path: "/admin/promotions", component: Promotions },
  { path: "/admin/reports", component: Reports }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

createApp(App).use(router).mount("#app");
