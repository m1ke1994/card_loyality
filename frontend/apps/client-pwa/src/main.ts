import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import App from "./App.vue";
import "./style.css";
import Dashboard from "./pages/Dashboard.vue";
import QrPage from "./pages/QrPage.vue";
import Visits from "./pages/Visits.vue";
import Transactions from "./pages/Transactions.vue";
import Rewards from "./pages/Rewards.vue";
import Settings from "./pages/Settings.vue";
import AuthTelegram from "./pages/AuthTelegram.vue";

const routes = [
  { path: "/", component: Dashboard },
  { path: "/auth/telegram", component: AuthTelegram },
  { path: "/qr", component: QrPage },
  { path: "/visits", component: Visits },
  { path: "/transactions", component: Transactions },
  { path: "/rewards", component: Rewards },
  { path: "/settings", component: Settings }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

createApp(App).use(router).mount("#app");
