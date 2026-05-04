<template>
  <div class="neural-core w-full h-full flex items-center justify-center animate-float">
    <svg viewBox="0 0 400 400" class="w-full h-full drop-shadow-[0_0_30px_rgba(34,211,238,0.2)]">
      <circle cx="200" cy="200" r="80" class="stroke-cyan-500/10 fill-none" stroke-width="0.5" />
      <circle cx="200" cy="200" r="120" class="stroke-cyan-500/5 fill-none" stroke-width="1" stroke-dasharray="8 12" />
      <circle cx="200" cy="200" r="30" class="fill-cyan-500/5 stroke-cyan-400/50" stroke-width="1">
        <animate attributeName="r" values="28;32;28" dur="4s" repeatCount="indefinite" />
      </circle>
      <g v-for="i in 12" :style="{ transform: `rotate(${i * 30}deg)`, transformOrigin: '200px 200px' }">
        <line x1="230" y1="200" x2="350" y2="200" class="stroke-cyan-500/20" stroke-width="0.5" />
        <circle cx="280" cy="200" r="1.5" class="fill-cyan-400">
          <animate attributeName="cx" values="230;340;230" :dur="2+Math.random()*2+'s'" repeatCount="indefinite" :begin="i*0.2+'s'" />
        </circle>
      </g>
    </svg>
  </div>
</template>

<script setup lang="ts">
// NeuralCore - Simulates neural network pulse
// Pure SVG declarative animation, zero JS runtime cost
</script>
