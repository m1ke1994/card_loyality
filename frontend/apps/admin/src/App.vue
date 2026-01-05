<template>
  <div class="min-h-screen bg-gradient-to-b from-slate-900 via-slate-950 to-black text-white">
    <header class="p-4 flex items-center justify-between">
      <div class="text-lg font-semibold">Admin</div>
      <nav class="flex gap-2 text-sm">
        <RouterLink v-for="link in links" :key="link.to" :to="link.to" class="px-3 py-1 rounded-full bg-white/10 hover:bg-white/20">
          {{ link.label }}
        </RouterLink>
      </nav>
    </header>
    <main class="p-4">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
const links = [
  { to: "/admin", label: "Обзор" },
  { to: "/admin/places", label: "Точки" },
  { to: "/admin/staff", label: "Персонал" },
  { to: "/admin/loyalty-rules", label: "Лояльность" },
  { to: "/admin/coupons", label: "Купоны" },
  { to: "/admin/promotions", label: "Промо" },
  { to: "/admin/reports", label: "Отчеты" }
];
</script>
