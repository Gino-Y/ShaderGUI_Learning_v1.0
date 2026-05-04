<template>
  <div class="perf-layer" v-if="activePerfSpec">
    <FlowPathDemo
      v-if="activePerfSpec.performanceType === 'demo' && activePerfSpec.demoType === 'flow-path'"
      :payload="activePerfSpec.payload"
      :duration-ms="perfDurationMs"
      :active="true"
    />
    <ParticleDecoration
      v-else-if="activePerfSpec.performanceType === 'decoration'"
      :payload="activePerfSpec.payload"
      :active="true"
    />
    <TransitionWipe
      v-else-if="activePerfSpec.performanceType === 'transition'"
      :payload="activePerfSpec.payload"
      :active="true"
    />
  </div>
</template>

<script setup>
import { computed } from "vue";
import FlowPathDemo from "./performances/FlowPathDemo.vue";
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

const perfDurationMs = computed(() => {
  if (!activePerfSpec.value) return 3000;
  const tr = activePerfSpec.value.timeRange || {};
  return tr.durationMs || (tr.end - tr.start) * 1000 || 3000;
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
