<template>
  <div class="p-6 text-center text-white">
    <div class="text-lg font-semibold">Авторизация...</div>
    <div class="text-white/60 text-sm">Telegram токен обрабатывается</div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

onMounted(async () => {
  const token = route.query.token as string;
  if (!token) {
    router.replace("/");
    return;
  }
  await fetch(`${import.meta.env.VITE_API_BASE_URL || "/api/proxy"}/api/v1/auth/telegram/consume`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token, tenant_slug: import.meta.env.VITE_TENANT_DEFAULT || "restaurant-slug" })
  });
  window.parent.postMessage({ type: "loyalty:auth" }, "*");
  router.replace("/");
});
</script>
