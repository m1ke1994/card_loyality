<template>
  <div class="space-y-3">
    <div v-for="visit in visits" :key="visit.id" class="rounded-2xl p-4 bg-white/5 border border-white/10 flex justify-between">
      <div>
        <div class="font-semibold">{{ visit.place }}</div>
        <div class="text-xs text-white/60">{{ visit.started_at }}</div>
      </div>
      <div class="text-right">
        <div class="text-emerald-300">+{{ visit.points_earned }} pts</div>
        <div class="text-white/60 text-xs">{{ visit.status }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const visits = [
  { id: 1, place: "Москва, Тверская", started_at: "2024-01-01", points_earned: 120, status: "closed" },
  { id: 2, place: "Москва, Покровка", started_at: "2024-01-03", points_earned: 80, status: "closed" }
];
</script>
