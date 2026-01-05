<template>
  <div class="min-h-screen bg-gradient-to-b from-slate-900 via-slate-950 to-black text-white">
    <header class="p-4 flex items-center justify-between">
      <div class="text-lg font-semibold">Loyalty</div>
      <nav class="flex gap-3 text-sm">
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
  { to: "/", label: "Dashboard" },
  { to: "/qr", label: "QR" },
  { to: "/visits", label: "Визиты" },
  { to: "/transactions", label: "Баллы" },
  { to: "/rewards", label: "Купоны" },
  { to: "/settings", label: "Настройки" }
];
</script>
