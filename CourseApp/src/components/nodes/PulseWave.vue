<template>
  <div class="pulse-wave relative w-full h-full flex items-center justify-center">
    <div v-for="i in 5" :key="i" 
         class="absolute w-64 h-64 border-2 border-cyan-500/40 rounded-full animate-pulse-wave shadow-[0_0_20px_rgba(34,211,238,0.2)]"
         :style="{ animationDelay: (i - 1) * 0.8 + 's' }">
    </div>
    <div class="w-4 h-4 bg-white rounded-full shadow-[0_0_30px_#fff] z-10 animate-pulse"></div>
  </div>
</template>

<script setup lang="ts">
// PulseWave - Outward radiating energy pulse field
// Multi-layer animation overlay for depth and rhythm
</script>

<style scoped>
@keyframes pulse-wave-out {
  0% { transform: scale(0.2); opacity: 0; }
  10% { opacity: 0.8; }
  100% { transform: scale(1.8); opacity: 0; }
}
.animate-pulse-wave {
  animation: pulse-wave-out 4s cubic-bezier(0.23, 1, 0.32, 1) infinite;
}
</style>
