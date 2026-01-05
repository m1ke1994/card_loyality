<template>
  <div>
    <div class="flex justify-between items-center mb-3">
      <div class="text-lg font-semibold">Промо</div>
      <button class="px-3 py-2 rounded-xl bg-emerald-500 text-white font-semibold">Добавить</button>
    </div>
    <div class="space-y-3">
      <div v-for="promo in promos" :key="promo.name" class="rounded-2xl p-4 bg-white/5 border border-white/10">
        <div class="font-semibold">{{ promo.name }}</div>
        <div class="text-sm text-white/70">{{ promo.rules }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const promos = [
  { name: "Happy Hours", rules: "+5% с 12:00 до 16:00" },
  { name: "Первый визит", rules: "+200 pts" }
];
</script>
