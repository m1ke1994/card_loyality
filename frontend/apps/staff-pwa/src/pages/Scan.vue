<template>
  <div class="space-y-4">
    <div class="rounded-3xl p-6 bg-white/5 border border-white/10 text-center">
      <div class="text-sm text-white/60 mb-2">Сканируйте QR гостя</div>
      <div class="h-64 bg-slate-900 rounded-2xl flex items-center justify-center border border-dashed border-white/20">
        <span class="text-white/40">Camera placeholder</span>
      </div>
      <div class="mt-4 text-3xl font-bold" :class="status === 'ok' ? 'text-emerald-400' : 'text-red-400'">
        {{ statusLabel }}
      </div>
      <div class="text-white/60 text-sm">Поднесите QR к камере. Токен одноразовый.</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";

const status = ref<"pending" | "ok" | "denied">("pending");
const statusLabel = computed(() => {
  if (status.value === "ok") return "OK — клиент найден";
  if (status.value === "denied") return "DENIED — другой визит активен";
  return "Ожидание";
});
</script>
