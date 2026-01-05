<template>
  <div class="grid gap-4 md:grid-cols-2">
    <div class="rounded-3xl p-6 bg-white/5 border border-white/10 shadow-soft">
      <div class="text-sm text-white/70 mb-2">Баланс</div>
      <div class="text-4xl font-bold">{{ balance.toLocaleString() }} баллов</div>
      <div class="mt-3 text-sm text-emerald-300">Текущий уровень: {{ tier }}</div>
    </div>
    <div class="rounded-3xl p-6 bg-gradient-to-r from-cyan-500/20 to-indigo-500/20 border border-white/10">
      <div class="text-sm text-white/80 mb-2">Быстрые действия</div>
      <div class="flex flex-wrap gap-2">
        <RouterLink v-for="action in actions" :key="action.to" :to="action.to" class="px-4 py-2 rounded-full bg-white/10 hover:bg-white/20">
          {{ action.label }}
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const balance = 4200;
const tier = "Silver";
const actions = [
  { to: "/qr", label: "Показать QR" },
  { to: "/rewards", label: "Купоны" },
  { to: "/visits", label: "Визиты" }
];
</script>
