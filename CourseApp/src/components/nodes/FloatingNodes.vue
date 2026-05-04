<template>
  <div class="floating-nodes relative w-full h-full flex items-center justify-center">
    <svg viewBox="0 0 400 400" class="w-full h-full opacity-40 text-white">
      <g v-for="i in 8" :key="i">
        <circle r="3" class="fill-current">
          <animate attributeName="cx" :values="Math.random()*400+';'+Math.random()*400+';'+Math.random()*400" dur="10s" repeatCount="indefinite" />
          <animate attributeName="cy" :values="Math.random()*400+';'+Math.random()*400+';'+Math.random()*400" dur="12s" repeatCount="indefinite" />
        </circle>
      </g>
      <path d="M 100,100 L 300,300 M 50,300 L 350,100" stroke="currentColor" stroke-width="0.5" stroke-dasharray="4 4" class="opacity-30" />
    </svg>
  </div>
</template>
