<template>
  <div>
    <div class="flex justify-between items-center mb-3">
      <div class="text-lg font-semibold">Персонал</div>
      <button class="px-3 py-2 rounded-xl bg-emerald-500 text-white font-semibold">Добавить</button>
    </div>
    <div class="space-y-3">
      <div v-for="staff in staffList" :key="staff.id" class="rounded-2xl p-4 bg-white/5 border border-white/10 flex justify-between">
        <div>
          <div class="font-semibold">{{ staff.name }}</div>
          <div class="text-xs text-white/60">Role: {{ staff.role }}</div>
        </div>
        <span class="text-white/60 text-xs">TG: {{ staff.telegram_user_id }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const staffList = [
  { id: 1, name: "Анна", role: "manager", telegram_user_id: "123" },
  { id: 2, name: "Иван", role: "cashier", telegram_user_id: "124" }
];
</script>
