<template>
  <canvas ref="canvasRef" class="particle-canvas"></canvas>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from "vue";

const props = defineProps({
  payload: { type: Object, default: () => ({}) },
  active: { type: Boolean, default: true },
});

const canvasRef = ref(null);
let animFrameId = null;
let particles = [];
let ctx = null;
let w = 0, h = 0;

function initParticles() {
  const count = props.payload?.count || 15;
  const colors = props.payload?.colors || ["#67e8f9", "#6ee7b7", "#a78bfa"];
  const [sMin, sMax] = props.payload?.speedRange || [0.2, 0.8];
  // 降低默认不透明度，避免遮挡卡片文字
  const [oMin, oMax] = props.payload?.opacityRange || [0.15, 0.4];

  particles = Array.from({ length: count }, () => ({
    x: Math.random() * w,
    y: Math.random() * h,
    r: 1.5 + Math.random() * 2.5,
    dx: (Math.random() - 0.5) * 0.6,
    dy: -(0.3 + Math.random() * 0.7),   // float upward
    color: colors[Math.floor(Math.random() * colors.length)],
    opacity: oMin + Math.random() * (oMax - oMin),
    phase: Math.random() * Math.PI * 2,
  }));
}

function tick(ts) {
  if (!ctx) return;
  ctx.clearRect(0, 0, w, h);
  for (const p of particles) {
    // Move
    p.x += p.dx;
    p.y += p.dy;
    // Wrap around
    if (p.y < -10) { p.y = h + 10; p.x = Math.random() * w; }
    if (p.x < -10) p.x = w + 10;
    if (p.x > w + 10) p.x = -10;
    // Pulse opacity
    const t = Math.sin(ts * 0.001 + p.phase) * 0.5 + 0.5;
    const alpha = p.opacity * (0.6 + 0.4 * t);
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx.fillStyle = p.color + Math.round(alpha * 255).toString(16).padStart(2, "0");
    ctx.fill();
    // Glow
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r * 2.5, 0, Math.PI * 2);
    ctx.fillStyle = p.color + Math.round(alpha * 60).toString(16).padStart(2, "0");
    ctx.fill();
  }
  animFrameId = requestAnimationFrame(tick);
}

function resize() {
  const canvas = canvasRef.value;
  if (!canvas) return;
  const parent = canvas.parentElement;
  w = parent ? parent.clientWidth : window.innerWidth;
  h = parent ? parent.clientHeight : window.innerHeight;
  canvas.width = w;
  canvas.height = h;
}

onMounted(() => {
  const canvas = canvasRef.value;
  if (!canvas) return;
  ctx = canvas.getContext("2d");
  resize();
  initParticles();
  animFrameId = requestAnimationFrame(tick);
  window.addEventListener("resize", resize);
});

onBeforeUnmount(() => {
  if (animFrameId) cancelAnimationFrame(animFrameId);
  window.removeEventListener("resize", resize);
});

watch(() => props.active, (val) => {
  if (val && !animFrameId) {
    animFrameId = requestAnimationFrame(tick);
  }
  if (!val && animFrameId) {
    cancelAnimationFrame(animFrameId);
    animFrameId = null;
  }
});
</script>

<style scoped>
.particle-canvas {
  width: 100%;
  height: 100%;
  pointer-events: none;
}
</style>
