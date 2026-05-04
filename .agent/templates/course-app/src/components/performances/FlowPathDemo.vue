<template>
  <div class="w-full flex items-center justify-center" style="max-height: 160px;">
    <svg class="w-full" viewBox="0 0 800 200" preserveAspectRatio="xMidYMid meet" style="max-height: 160px;">
    <!-- Edges (paths with flowing dash animation) -->
    <g v-for="(edge, ei) in edgesWithPos" :key="'edge-' + ei">
      <path
        :d="edge.d"
        fill="none"
        :stroke="payload.style?.accentColor || '#67e8f9'"
        stroke-width="2"
        :stroke-dasharray="edge.len"
        :stroke-dashoffset="edge.len"
        :style="{ animation: `drawPath ${animDuration}s ${ei * 0.3}s ease forwards, glowPulse 2s ${ei * 0.3 + 0.5}s ease-in-out infinite alternate` }"
        class="edge-path"
      />
      <text
        :x="edge.labelX"
        :y="edge.labelY"
        fill="#94a3b8"
        font-size="12"
        class="edge-label"
      >{{ edge.label }}</text>
    </g>

    <!-- Nodes -->
    <g v-for="(node, ni) in nodesWithPos" :key="'node-' + ni">
      <circle
        :cx="node.x"
        :cy="node.y"
        :r="node.r"
        :fill="node.fill"
        :stroke="payload.style?.accentColor || '#67e8f9'"
        stroke-width="2"
        :style="{ animation: `nodeAppear 0.5s ${ni * 0.25}s ease both, nodeGlow 2s ${ni * 0.3}s ease-in-out infinite alternate` }"
        class="node-circle"
      />
      <text
        :x="node.x"
        :y="node.y + 5"
        fill="#e2e8f0"
        font-size="14"
        font-weight="600"
        text-anchor="middle"
        :style="{ animation: `nodeAppear 0.5s ${ni * 0.25 + 0.1}s ease both` }"
      >{{ node.label }}</text>
    </g>

    <!-- Floating particles along edges -->
    <circle
      v-for="(p, pi) in particles"
      :key="'p-' + pi"
      :cx="p.x"
      :cy="p.y"
      r="3"
      :fill="payload.style?.accentColor || '#67e8f9'"
      :style="{ opacity: 0.7, animation: `particleDrift ${p.dur}s ${p.delay}s ease-in-out infinite alternate` }"
    />
  </svg>
  </div>
</template>

<script setup>
import { computed, ref, watch, onMounted } from "vue";

const props = defineProps({
  payload: { type: Object, default: () => ({}) },
  durationMs: { type: Number, default: 3000 },
  active: { type: Boolean, default: true },
});

const animDuration = computed(() => Math.max(1.5, (props.durationMs || 3000) / 1000 - 0.5));

// Node positions (simple horizontal layout)
const nodes = computed(() => props.payload?.nodes || []);
const edges = computed(() => props.payload?.edges || []);

const NODE_R = 32;
const SVG_W = 800, SVG_H = 200;
const PAD = 80;

const nodesWithPos = computed(() => {
  const ns = nodes.value;
  if (!ns.length) return [];
  const gap = (SVG_W - PAD * 2) / Math.max(1, ns.length - 1);
  return ns.map((n, i) => ({
    ...n,
    x: PAD + i * gap,
    y: SVG_H / 2,
    r: NODE_R,
    fill: n.type === "source" ? "rgba(103,232,249,0.15)" :
         n.type === "target" ? "rgba(110,231,183,0.15)" :
         "rgba(167,139,250,0.15)",
  }));
});

// Build edge paths (quadratic bezier)
const edgesWithPos = computed(() => {
  const ns = nodesWithPos.value;
  return edges.value.map((e) => {
    const from = ns.find((n) => n.id === e.from);
    const to = ns.find((n) => n.id === e.to);
    if (!from || !to) return null;
    const mx = (from.x + to.x) / 2;
    const d = `M ${from.x} ${from.y} Q ${mx} ${from.y - 60}, ${to.x} ${to.y}`;
    // Approx length
    const len = Math.sqrt((to.x - from.x) ** 2 + (to.y - from.y) ** 2) + 40;
    return {
      ...e,
      d,
      len: Math.round(len),
      labelX: mx,
      labelY: (from.y + to.y) / 2 - 70,
    };
  }).filter(Boolean);
});

// Simple particles that float near edges
const particles = computed(() => {
  const count = props.payload?.style?.particleCount || 12;
  const arr = [];
  for (let i = 0; i < count; i++) {
    arr.push({
      x: 100 + Math.random() * 600,
      y: SVG_H / 2 - 20 + Math.random() * 40,
      dur: 1.5 + Math.random() * 2,
      delay: Math.random() * 2,
    });
  }
  return arr;
});
</script>

<style scoped>
@keyframes drawPath {
  0% { stroke-dashoffset: var(--len, 200); }
  100% { stroke-dashoffset: 0; }
}
@keyframes glowPulse {
  0% { filter: drop-shadow(0 0 3px rgba(103,232,249,0.3)); }
  100% { filter: drop-shadow(0 0 10px rgba(103,232,249,0.7)); }
}
@keyframes nodeAppear {
  0% { opacity: 0; transform: scale(0.5); }
  100% { opacity: 1; transform: scale(1); }
}
@keyframes nodeGlow {
  0% { filter: drop-shadow(0 0 2px rgba(103,232,249,0.2)); }
  100% { filter: drop-shadow(0 0 8px rgba(103,232,249,0.6)); }
}
@keyframes particleDrift {
  0% { transform: translateX(0) translateY(0); opacity: 0.4; }
  100% { transform: translateX(15px) translateY(-8px); opacity: 0.8; }
}
.flow-path-demo {
  width: 100%;
  height: 100%;
}
.edge-path {
  /* stroke-dasharray/offset driving by JS to work around v-bind limitation */
}
</style>
