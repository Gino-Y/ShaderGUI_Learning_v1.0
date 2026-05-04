<template>
  <div class="particle-vortex relative w-full h-full flex items-center justify-center">
    <svg viewBox="0 0 400 400" class="w-full h-full opacity-60">
      <g v-for="i in 60" :key="i" :style="{ transform: `rotate(${i * 6}deg)`, transformOrigin: '200px 200px' }">
        <circle r="1" cx="200" class="fill-white">
          <animate attributeName="cy" :values="Math.random()*100 + 50 + ';200;' + (Math.random()*100+50)" :dur="2+Math.random()*3+'s'" repeatCount="indefinite" :begin="Math.random()*5+'s'" />
          <animate attributeName="opacity" values="0;1;0" :dur="2+Math.random()*3+'s'" repeatCount="indefinite" />
        </circle>
      </g>
    </svg>
  </div>
</template>
