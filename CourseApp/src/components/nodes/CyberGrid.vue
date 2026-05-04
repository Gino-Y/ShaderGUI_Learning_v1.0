<template>
  <div class="cyber-grid relative w-full h-full flex items-center justify-center overflow-hidden rounded-[40px]">
    <div class="absolute inset-0 cyber-grid-base scale-[2] origin-center"></div>
    <div class="absolute left-0 right-0 h-40 bg-gradient-to-b from-transparent via-cyan-400/40 to-transparent animate-scan-wave z-10">
      <div class="absolute bottom-0 left-0 right-0 h-[2px] bg-cyan-300 shadow-[0_0_20px_#22d3ee]"></div>
    </div>
    <div v-for="i in 15" :key="i" 
         class="absolute w-1 h-1 bg-cyan-400 rounded-full animate-data-point"
         :style="{ left: Math.random() * 80 + 10 + '%', top: Math.random() * 80 + 10 + '%', animationDelay: Math.random() * 5 + 's' }">
    </div>
    <div class="z-20 text-center">
      <p class="text-[10px] font-mono tracking-[0.5em] text-cyan-400/60 mb-2 uppercase">System Scanning</p>
      <div class="flex items-baseline gap-1">
        <span class="text-4xl font-black italic text-white tracking-tighter">0.42</span>
        <span class="text-xs font-bold text-cyan-400 uppercase tracking-widest">ms</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// CyberGrid - Enhanced perspective scan engine
// Includes multi-layer light/shadow, scan beam, data nodes
</script>

<style scoped>
@keyframes grid-move {
  0% { transform: perspective(500px) rotateX(60deg) translateY(0); }
  100% { transform: perspective(500px) rotateX(60deg) translateY(50px); }
}
.cyber-grid-base {
  background-image: 
    linear-gradient(rgba(34, 211, 238, 0.2) 1px, transparent 1px),
    linear-gradient(90deg, rgba(34, 211, 238, 0.2) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: grid-move 2s linear infinite;
}

@keyframes scan-wave {
  0% { top: -10%; opacity: 0; }
  5% { opacity: 1; }
  95% { opacity: 1; }
  100% { top: 110%; opacity: 0; }
}
.animate-scan-wave {
  animation: scan-wave 4s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes data-flicker {
  0%, 100% { opacity: 0.2; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.5); }
}
.animate-data-point {
  animation: data-flicker 2s ease-in-out infinite;
}
</style>
