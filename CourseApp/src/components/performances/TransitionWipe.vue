<template>
  <transition name="wipe" appear>
    <div v-if="active" class="wipe-overlay"></div>
  </transition>
</template>

<script setup>
defineProps({
  payload: { type: Object, default: () => ({}) },
  active: { type: Boolean, default: true },
});
</script>

<style scoped>
.wipe-overlay {
  position: absolute;
  inset: 0;
  z-index: 100;
  pointer-events: none;
  background: linear-gradient(
    90deg,
    rgba(103, 232, 249, 0.12) 0%,
    rgba(103, 232, 249, 0.04) 100%
  );
}
.wipe-enter-active,
.wipe-leave-active {
  transition: opacity 0.6s ease;
}
.wipe-enter-from,
.wipe-leave-to {
  opacity: 0;
}
</style>
