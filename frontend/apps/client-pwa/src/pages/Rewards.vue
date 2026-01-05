<template>
  <div class="grid gap-3 md:grid-cols-2">
    <div v-for="coupon in coupons" :key="coupon.code" class="rounded-2xl p-4 bg-white/5 border border-white/10">
      <div class="text-sm text-white/60 mb-1">{{ coupon.type }}</div>
      <div class="text-xl font-semibold mb-2">{{ coupon.code }}</div>
      <div class="text-white/70 text-sm">{{ coupon.desc }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
const coupons = [
  { code: "WELCOME10", type: "percent", desc: "-10% на первый визит" },
  { code: "COFFEE", type: "gift", desc: "Кофе в подарок" }
];
</script>
