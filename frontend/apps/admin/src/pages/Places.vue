<template>
  <div>
    <div class="flex justify-between items-center mb-3">
      <div class="text-lg font-semibold">Точки</div>
      <button class="px-3 py-2 rounded-xl bg-emerald-500 text-white font-semibold">Добавить</button>
    </div>
    <div class="space-y-3">
      <div v-for="place in places" :key="place.id" class="rounded-2xl p-4 bg-white/5 border border-white/10 flex justify-between">
        <div>
          <div class="font-semibold">{{ place.name }}</div>
          <div class="text-xs text-white/60">{{ place.address }}</div>
        </div>
        <span class="text-emerald-300 text-xs">Активна</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const places = [
  { id: 1, name: "Москва, Тверская", address: "ул. Тверская, 12" },
  { id: 2, name: "Москва, Покровка", address: "ул. Покровка, 17" }
];
</script>
