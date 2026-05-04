<template>
  <div class="data-prism perspective-2000 w-full h-full flex items-center justify-center">
    <div class="preserve-3d animate-cube relative w-40 h-40">
      <div v-for="i in 6" :key="i" :style="getFaceStyle(i)" 
           class="absolute inset-0 bg-purple-500/10 border border-purple-400/40 backdrop-blur-md flex items-center justify-center">
        <div class="w-8 h-8 rounded-full border border-purple-200/20 animate-pulse"></div>
      </div>
      <div class="absolute inset-4 bg-purple-500/30 blur-3xl rounded-full"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
function getFaceStyle(i: number) {
  const transforms = [
    'rotateY(0deg) translateZ(80px)', 'rotateY(180deg) translateZ(80px)',
    'rotateY(90deg) translateZ(80px)', 'rotateY(-90deg) translateZ(80px)',
    'rotateX(90deg) translateZ(80px)', 'rotateX(-90deg) translateZ(80px)'
  ];
  return { transform: transforms[i - 1] };
}
</script>

<style scoped>
@keyframes cube-rotate {
  from { transform: rotateX(45deg) rotateY(45deg); }
  to { transform: rotateX(405deg) rotateY(765deg); }
}
.animate-cube {
  animation: cube-rotate 20s linear infinite;
}
</style>
