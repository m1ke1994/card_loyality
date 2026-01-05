<template>
  <div class="space-y-3">
    <div v-for="tx in txs" :key="tx.id" class="rounded-2xl p-4 bg-white/5 border border-white/10 flex justify-between">
      <div>
        <div class="font-semibold capitalize">{{ tx.type }}</div>
        <div class="text-xs text-white/60">{{ tx.created_at }}</div>
      </div>
      <div :class="tx.points > 0 ? 'text-emerald-300' : 'text-red-300'">
        {{ tx.points > 0 ? '+' : '' }}{{ tx.points }} pts
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const txs = [
  { id: 1, type: "earn", points: 120, created_at: "2024-01-01" },
  { id: 2, type: "spend", points: -80, created_at: "2024-01-03" }
];
</script>
