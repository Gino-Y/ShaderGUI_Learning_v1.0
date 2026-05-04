<template>
  <div class="aurora-fluid relative w-full h-full blur-[60px] opacity-40">
    <div class="absolute top-1/4 left-1/4 w-64 h-64 bg-rose-500 rounded-full animate-float"></div>
    <div class="absolute bottom-1/4 right-1/4 w-80 h-80 bg-blue-600 rounded-full animate-float" style="animation-delay: -3s"></div>
  </div>
</template>

<script setup lang="ts">
// AuroraFluid - Abstract fluid simulation
// High-order Gaussian blur with color blending
</script>

<style scoped>
@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(2deg); }
}
.animate-float { animation: float 6s ease-in-out infinite; }
</style>
