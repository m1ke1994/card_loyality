<template>
  <div>
    <div class="flex justify-between items-center mb-3">
      <div class="text-lg font-semibold">Купоны</div>
      <button class="px-3 py-2 rounded-xl bg-emerald-500 text-white font-semibold">Добавить</button>
    </div>
    <div class="grid gap-3 md:grid-cols-2">
      <div v-for="coupon in coupons" :key="coupon.code" class="rounded-2xl p-4 bg-white/5 border border-white/10">
        <div class="text-sm text-white/60">{{ coupon.type }}</div>
        <div class="text-xl font-semibold">{{ coupon.code }}</div>
        <div class="text-white/70 text-sm">{{ coupon.desc }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const coupons = [
  { code: "WELCOME10", type: "percent", desc: "-10% на первый визит" },
  { code: "COFFEE", type: "gift", desc: "Кофе в подарок" }
];
</script>
