<template>
  <div class="max-w-md mx-auto space-y-4">
    <div class="rounded-3xl p-6 bg-white/5 border border-white/10 text-center">
      <div class="text-sm text-white/70 mb-2">Одноразовый QR</div>
      <canvas ref="canvasRef" class="mx-auto"></canvas>
      <div class="mt-3 text-xs text-white/50">Автообновление каждые 20 сек · TTL 30 сек</div>
      <div class="mt-2 text-emerald-300 text-sm">{{ statusText }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from "vue";
import QRCode from "qrcode";

const canvasRef = ref<HTMLCanvasElement | null>(null);
const statusText = ref("");
let timer: any;

async function refreshQr() {
  statusText.value = "Запрос токена...";
  const res = await fetch(`${import.meta.env.VITE_API_BASE_URL || "/api/proxy"}/api/v1/tokens/issue/`, { method: "POST", credentials: "include" });
  if (!res.ok) {
    statusText.value = "Ошибка загрузки";
    return;
  }
  const data = await res.json();
  const payload = JSON.stringify({ qr_token: data.qr_token, ts: Date.now() });
  if (canvasRef.value) {
    await QRCode.toCanvas(canvasRef.value, payload, { width: 240, margin: 1 });
  }
  statusText.value = "Готово";
}

onMounted(() => {
  refreshQr();
  timer = setInterval(refreshQr, 20000);
});

onUnmounted(() => clearInterval(timer));
</script>
