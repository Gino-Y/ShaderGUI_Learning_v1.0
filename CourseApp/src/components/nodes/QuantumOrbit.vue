<template>
  <div class="quantum-orbit relative w-full h-full flex items-center justify-center">
    <svg viewBox="0 0 400 400" class="w-full h-full">
      <ellipse cx="200" cy="200" rx="140" ry="60" class="stroke-white/10 fill-none" stroke-width="1" transform="rotate(45 200 200)" />
      <ellipse cx="200" cy="200" rx="140" ry="60" class="stroke-white/10 fill-none" stroke-width="1" transform="rotate(-45 200 200)" />
      <circle cx="200" cy="200" r="10" class="fill-white shadow-xl animate-pulse" />
      <circle r="4" class="fill-cyan-400">
         <animateMotion dur="4s" repeatCount="indefinite" path="M 60,200 A 140,60 45 1,1 340,200 A 140,60 45 1,1 60,200" />
      </circle>
    </svg>
  </div>
</template>
