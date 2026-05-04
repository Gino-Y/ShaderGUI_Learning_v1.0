<template>
  <div class="fractal-dna h-64 w-32 flex items-center justify-center">
    <svg viewBox="0 0 100 200" class="w-full h-full">
      <g v-for="i in 10" :key="i">
        <circle :cy="i*20" r="4" class="fill-rose-500">
          <animate attributeName="cx" values="20;80;20" dur="2s" repeatCount="indefinite" :begin="i*0.2+'s'" />
        </circle>
        <circle :cy="i*20" r="4" class="fill-blue-500">
          <animate attributeName="cx" values="80;20;80" dur="2s" repeatCount="indefinite" :begin="i*0.2+'s'" />
        </circle>
        <line :y1="i*20" :y2="i*20" class="stroke-white/20" stroke-width="1">
          <animate attributeName="x1" values="20;80;20" dur="2s" repeatCount="indefinite" :begin="i*0.2+'s'" />
          <animate attributeName="x2" values="80;20;80" dur="2s" repeatCount="indefinite" :begin="i*0.2+'s'" />
        </line>
      </g>
    </svg>
  </div>
</template>
