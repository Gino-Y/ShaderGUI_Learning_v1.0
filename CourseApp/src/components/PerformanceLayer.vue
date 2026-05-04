<template>
  <div class="perf-layer" v-if="activePerfSpec">
    <!-- 毛玻璃背景层：让底部内容隐约可见 -->
    <div class="perf-backdrop"></div>

    <FlowPathDemo
      v-if="activePerfSpec.performanceType === 'demo' && activePerfSpec.demoType === 'flow-path'"
      :payload="activePerfSpec.payload"
      :duration-ms="perfDurationMs"
      :active="true"
      class="perf-content"
    />
    <ParticleDecoration
      v-else-if="activePerfSpec.performanceType === 'decoration'"
      :payload="activePerfSpec.payload"
      :active="true"
      class="perf-content"
    />
    <TransitionWipe
      v-else-if="activePerfSpec.performanceType === 'transition'"
      :payload="activePerfSpec.payload"
      :active="true"
      class="perf-content"
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
  z-index: 20;
}

/* 毛玻璃背景：让底部内容隐约可见，同时不抢夺视觉焦点 */
.perf-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.35);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  z-index: 1;
  pointer-events: none;
}

/* 表演内容层：半透明，不抢夺文字可读性 */
:deep(.perf-content) {
  position: relative;
  z-index: 2;
  opacity: 0.6;
}
</style>
