<template>
  <div class="holographic-hud relative w-full h-full flex items-center justify-center text-emerald-400">
    <svg viewBox="0 0 400 400" class="w-full h-full">
      <circle cx="200" cy="200" r="100" class="stroke-current fill-none opacity-20" stroke-width="0.5" stroke-dasharray="10 5" />
      <path d="M 200,60 A 140,140 0 0,1 340,200" class="stroke-current fill-none" stroke-width="3" stroke-linecap="round">
        <animateTransform attributeName="transform" type="rotate" from="0 200 200" to="360 200 200" dur="10s" repeatCount="indefinite" />
      </path>
      <path d="M 200,340 A 140,140 0 0,1 60,200" class="stroke-current fill-none opacity-30" stroke-width="8" stroke-linecap="round">
        <animateTransform attributeName="transform" type="rotate" from="360 200 200" to="0 200 200" dur="15s" repeatCount="indefinite" />
      </path>
      <text x="200" y="200" text-anchor="middle" dominant-baseline="middle" class="fill-current font-mono text-2xl animate-pulse">ANALYZING</text>
    </svg>
  </div>
</template>
