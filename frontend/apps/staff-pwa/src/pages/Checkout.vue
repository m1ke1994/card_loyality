<template>
  <div class="rounded-2xl p-4 bg-white/5 border border-white/10 space-y-3 max-w-md">
    <div class="text-lg font-semibold">Checkout визита {{ $route.params.visit_id }}</div>
    <label class="block">
      <span class="text-sm text-white/70">Сумма</span>
      <input v-model="amount" type="number" class="mt-1 w-full rounded-xl bg-white/10 border border-white/20 px-3 py-2" />
    </label>
    <label class="block">
      <span class="text-sm text-white/70">Списать баллы</span>
      <input v-model="points" type="number" class="mt-1 w-full rounded-xl bg-white/10 border border-white/20 px-3 py-2" />
    </label>
    <button class="w-full rounded-xl bg-gradient-to-r from-emerald-500 to-cyan-500 py-3 font-semibold" @click="complete">
      Завершить
    </button>
    <div v-if="status" class="text-emerald-300 text-sm">{{ status }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const amount = ref(0);
const points = ref(0);
const status = ref("");

function complete() {
  status.value = "Завершено (mock)";
}
</script>
