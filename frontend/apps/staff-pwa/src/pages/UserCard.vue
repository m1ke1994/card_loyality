<template>
  <div class="rounded-2xl p-4 bg-white/5 border border-white/10 space-y-3">
    <div class="text-lg font-semibold">Клиент #{{ $route.params.id }}</div>
    <div class="text-white/70">Баланс: 4200 pts · Tier: Silver</div>
    <RouterLink :to="`/staff/checkout/${$route.params.id}`" class="px-4 py-2 rounded-full bg-emerald-500 text-white font-semibold">
      Checkout
    </RouterLink>
  </div>
</template>
