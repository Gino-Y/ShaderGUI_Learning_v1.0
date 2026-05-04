<template>
  <div class="min-h-[96px] rounded-md border border-white/10 bg-neutral-900/95 px-5 py-4 text-center shadow-2xl">
    <p class="mx-auto max-w-5xl text-xl font-medium leading-9 text-white sm:text-2xl">{{ text || " " }}</p>
  </div>
</template>
<script setup>
defineProps({ text: { type: String, default: "" } });
</script>
