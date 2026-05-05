<template>
  <div class="perf-layer" v-if="activePerfSpec">
    <ParticleDecoration
      v-if="activePerfSpec.type === 'decoration'"
      :payload="activePerfSpec.payload"
      :active="true"
    />
    <TransitionWipe
      v-else-if="activePerfSpec.type === 'transition'"
      :payload="activePerfSpec.payload"
      :active="true"
    />
  </div>
</template>

<script setup>
import { computed } from "vue";
import ParticleDecoration from "./performances/ParticleDecoration.vue";
import TransitionWipe from "./performances/TransitionWipe.vue";

const props = defineProps({
  perfSpecs: { type: Array, default: () => [] },
  currentTime: { type: Number, default: 0 },
});

const activePerfSpec = computed(() => {
  const t = props.currentTime;
  return props.perfSpecs.find((ps) => {
    const start = ps.timeRange?.start ?? 0;
    const end = ps.timeRange?.end ?? start + 3;
    return t >= start && t < end;
  }) || null;
});
</script>

<style scoped>
.perf-layer {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: -1;
}
</style>
