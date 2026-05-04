<template>
  <article class="relative isolate min-h-[560px] overflow-hidden rounded-[2rem] border border-white/10 bg-slate-950 p-6 text-white shadow-2xl shadow-cyan-950/30">
    <div class="absolute -left-24 -top-24 h-72 w-72 rounded-full bg-cyan-500/20 blur-3xl"></div>
    <div class="absolute -bottom-28 right-0 h-80 w-80 rounded-full bg-emerald-500/10 blur-3xl"></div>

    <div class="relative grid min-h-[512px] gap-6" :class="compositionGridClass" :data-shot-type="composition?.shotType || 'slide'">
      <section class="flex flex-col justify-between rounded-[1.5rem] border border-white/10 bg-white/[0.06] p-6 backdrop-blur" :data-frame-zone="foregroundZone">
        <div>
          <div class="flex flex-wrap items-center gap-3">
            <span class="rounded-full border border-cyan-300/30 bg-cyan-300/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-cyan-200">
              {{ slide.moduleId }} / {{ slide.slideId }}
            </span>
            <span class="rounded-full bg-white/10 px-3 py-1 text-xs text-slate-300">{{ slide.kind || "concept" }}</span>
            <span v-if="activeVisualSpec" class="rounded-full bg-emerald-300/10 px-3 py-1 text-xs text-emerald-200">
              {{ activeVisualSpec.animation?.type }} · {{ activeVisualSpec.compositionBeat?.frameZone }}
            </span>
          </div>
          <h1 class="mt-6 max-w-3xl text-4xl font-semibold leading-tight tracking-tight text-white sm:text-5xl">
            {{ slide.title }}
          </h1>
          <p class="mt-5 max-w-2xl text-base leading-7 text-slate-300">
            {{ leadText }}
          </p>
        </div>

        <div class="mt-8 grid gap-3">
          <div
            v-for="(point, index) in slide.points"
            :key="point"
            :data-composition-zone="pointFrameZone(index)"
            class="point-card group rounded-2xl border border-white/10 bg-slate-900/80 p-4 transition duration-500 hover:border-cyan-300/50 hover:bg-slate-900"
            :class="pointCueClass(point)"
            :style="pointCardStyle(point, index)"
          >
            <div class="flex gap-4">
              <span class="grid h-8 w-8 shrink-0 place-items-center rounded-full text-sm font-bold transition duration-500" :class="pointBadgeClass(point)">
                {{ index + 1 }}
              </span>
              <p class="text-lg leading-7 text-slate-100">
                <span class="inline rounded-lg px-2 py-1 transition duration-500" :class="textCueClass(point)">
                  {{ point }}
                </span>
              </p>
            </div>
          </div>
        </div>
      </section>

      <aside class="grid gap-4" :data-frame-zone="midgroundZone">
        <div v-if="codeBlocks.length" class="grid gap-4" :data-composition-zone="codeFrameZone">
          <div
            v-for="block in codeBlocks"
            :key="block.title"
            class="rounded-[1.5rem] border border-emerald-300/20 bg-[#07111f] p-5 shadow-inner shadow-black/40"
          >
            <div class="mb-4 flex items-center justify-between text-xs text-slate-400">
              <span>{{ block.title }}</span>
              <span class="text-emerald-300">{{ block.badge }}</span>
            </div>
            <pre class="max-h-[280px] overflow-auto rounded-xl border bg-black/35 p-4 text-sm leading-6 text-emerald-100 transition duration-500" :class="codeBlockCueClass(block)"><code><span v-for="(line, lineIndex) in codeLines(block)" :key="`${block.title}-${lineIndex}-${line}`" class="block"><span v-for="(part, partIndex) in splitCodeLine(line)" :key="`${block.title}-${lineIndex}-${partIndex}-${part.text}`" :class="codeFieldCueClass(part.text)">{{ part.text || " " }}</span></span></code></pre>
          </div>
        </div>
        <div v-if="mentalModelVisible" class="rounded-[1.5rem] border border-white/10 bg-white/[0.06] p-5">
          <p class="text-sm font-semibold text-cyan-200">{{ mentalModelTitle }}</p>
          <p class="mt-3 text-sm leading-6 text-slate-300">{{ mentalModelText }}</p>
        </div>
        <div v-if="learnerFocusVisible" class="rounded-[1.5rem] border border-white/10 bg-slate-900/80 p-5">
          <p class="text-sm font-semibold text-emerald-200">{{ storyboardEmphasisLabel }}</p>
          <p class="mt-3 text-2xl font-semibold leading-snug text-white">{{ storyboardEmphasisText }}</p>
        </div>
      </aside>

      <!-- FlowPathDemo 与主卡片同级，跨满 grid 宽度 -->
      <section
        v-if="showFlowPath"
        :key="activePerfSpec?.cueId"
        class="rounded-[1.5rem] border border-cyan-300/20 bg-slate-950/80 px-4 py-1"
        style="grid-column: 1 / -1"
      >
        <FlowPathDemo
          :payload="activePerfSpec.payload"
          :duration-ms="perfDurationMs"
          :active="true"
        />
      </section>

    </div>

    <!-- 表演层：仅背景粒子，z-index: -1，不影响排版 -->
    <PerformanceLayer
      :perf-specs="performanceSpecs"
      :current-time="currentTime"
    />
  </article>
</template>
<script setup>
import { computed, watch } from "vue";
import PerformanceLayer from "./PerformanceLayer.vue";
import FlowPathDemo from "./performances/FlowPathDemo.vue";

const props = defineProps({
  slide: { type: Object, required: true },
  activeCue: { type: Object, default: null },
  composition: { type: Object, default: null },
  motionCues: { type: Array, default: () => [] },
  visualSpecs: { type: Array, default: () => [] },
  performanceSpecs: { type: Array, default: () => [] },
  currentTime: { type: Number, default: 0 },
});

// 当前激活的表演规范（供模板条件渲染 FlowPathDemo）
const activePerfSpec = computed(() => {
  const t = props.currentTime;
  return props.performanceSpecs.find((ps) => {
    const start = ps.timeRange?.start ?? 0;
    const end = ps.timeRange?.end ?? start + 3;
    return t >= start && t < end;
  }) || null;
});

const showFlowPath = computed(
  () =>
    activePerfSpec.value?.performanceType === "demo" &&
    activePerfSpec.value?.demoType === "flow-path"
);

const perfDurationMs = computed(() => {
  if (!activePerfSpec.value) return 3000;
  const tr = activePerfSpec.value.timeRange || {};
  return tr.durationMs || (tr.end - tr.start) * 1000 || 3000;
});
const activeVisualSpec = computed(() => {
  if (!props.activeCue || !props.visualSpecs?.length) return null;
  return props.visualSpecs.find((spec) => spec.cueId === props.activeCue.cueId) || null;
});

// 供 <style scoped> v-bind() 使用
const animDuration = computed(() => (activeVisualSpec.value?.animation?.durationMs ?? 420) + "ms");
const animEasing = computed(() => activeVisualSpec.value?.animation?.easing ?? "ease-out");
// 当前视觉激活对应的知识点文本
const visualActivePoint = computed(() => {
  const spec = activeVisualSpec.value;
  if (!spec) return null;
  return spec.knowledgeFocus?.label || spec.contentBeat || null;
});

// 每个 point-card 的装饰样式
// 注意：opacity/transform 的动画完全由 CSS @keyframes reveal-focus 驱动
// 这里只负责：非激活卡片的暗化 + 激活卡片的装饰效果（阴影、边框）
function pointCardStyle(point, index) {
  const spec = activeVisualSpec.value;
  // 没有激活的 spec：所有卡片统一暗化
  if (!spec) return { opacity: 0.82 };
  const label = spec.knowledgeFocus?.label || spec.contentBeat || "";
  const isMatch = label.includes(point) || point.includes(label.slice(0, 10));
  // 不匹配：进一步暗化
  if (!isMatch) return { opacity: 0.55 };
  // 匹配卡片：不碰 opacity/transform（交给 CSS animation），只加装饰
  const visual = spec.dynamicGuidance?.visualTreatment || {};
  const glow = visual.glow ? "0 0 18px 3px rgba(103,232,249,0.35)" : "none";
  return {
    boxShadow: glow,
    borderColor: "rgba(103,232,249,0.55)",
  };
}

watch(() => activeVisualSpec.value, (newSpec) => {
  if (newSpec) {
    console.log('[VisualSpec] active:', newSpec.cueId, newSpec.animation?.type, newSpec.compositionBeat?.frameZone);
  }
});
const leadText = computed(() => props.slide.points?.[0] || "围绕 ShaderGUI 的工程化表达建立清晰的学习路径。");
const mentalModel = computed(() => props.slide.mentalModel || {});
const mentalModelTitle = computed(() => mentalModel.value.title || "");
const mentalModelText = computed(() => mentalModel.value.text || "");
const mentalModelVisible = computed(() => mentalModelTitle.value && mentalModelText.value);
const storyboardEmphasisLabel = "当前强调";
const storyboardEmphasisText = computed(() => {
  const cue = props.activeCue;
  if (!cue) return "";
  return cue.knowledgeFocus?.label || cue.contentBeat || "";
});
const learnerFocusVisible = computed(() => Boolean(storyboardEmphasisText.value));
const codeBlocks = computed(() => {
  if (props.slide.codeBlocks?.length) return props.slide.codeBlocks;
  if (!props.slide.code) return [];
  return [{ title: "MyGUI.cs", language: "csharp", badge: "C# side", code: props.slide.code }];
});
const activeCodeFields = computed(() => {
  if (props.activeCue?.dynamicGuidance?.primaryEffect !== "code-highlight") return [];
  const tokens = props.activeCue?.dynamicGuidance?.codeHighlightTokens;
  if (Array.isArray(tokens) && tokens.length) {
    return [...tokens].sort((a, b) => b.length - a.length);
  }
  const label = props.activeCue.knowledgeFocus?.label || props.activeCue.contentBeat || "";
  if (label.includes("继承") || label.includes("重写")) return ["ShaderGUI", "OnGUI"];
  if (label.includes("CustomEditor")) return ["CustomEditor", "MyGUI"];
  if (label.includes("高级面板能力") || label.includes("控制 OnGUI")) return ["OnGUI", "FindProperty", "ShaderProperty", "MaterialProperty"];
  return [];
});
const compositionGridClass = computed(() => {
  const columns = props.composition?.frameGrid?.columns || "";
  if (columns.includes("left 56%") && columns.includes("right 44%")) return "lg:grid-cols-[1.27fr_1fr]";
  if (columns.includes("left 48%") && columns.includes("right 52%")) return "lg:grid-cols-[0.92fr_1fr]";
  return "lg:grid-cols-[1.05fr_0.95fr]";
});
const foregroundZone = computed(() => props.composition?.foreground?.position || "foreground");
const midgroundZone = computed(() => props.composition?.midground?.position || "midground");
const codeFrameZone = computed(() => props.activeCue?.compositionBeat?.frameZone || "code-panel");

function isActivePoint(point) {
  if (!props.activeCue) return false;
  const label = (props.activeCue.knowledgeFocus?.label || props.activeCue.contentBeat || "").trim();
  if (!label) return false;
  return label.includes(point) || point.includes(label);
}

function pointCueClass(point) {
  if (!props.activeCue) return "";
  if (isActivePoint(point)) {
    const zone = props.activeCue.compositionBeat?.frameZone || "";
    return zone.includes("hero") || zone.includes("card")
      ? "ring-1 ring-cyan-200/60 shadow-lg shadow-cyan-500/20"
      : "";
  }
  return props.activeCue?.dynamicGuidance?.deEmphasizeOthers ? "opacity-45" : "";
}

function pointFrameZone(index) {
  if (props.slide.kind === "code") return index === 0 ? "left principle stack" : "supporting principle stack";
  return index === 0 ? "left hero concept" : `right support card ${index}`;
}

function pointBadgeClass(point) {
  return isActivePoint(point) ? "bg-cyan-200 text-slate-950" : "bg-cyan-300 text-slate-950";
}

function textCueClass(point) {
  if (!isActivePoint(point)) return "";
  const shouldBlink = props.activeCue?.dynamicGuidance?.visualTreatment?.blink;
  return [
    "bg-cyan-300/15 text-white shadow-lg shadow-cyan-500/20 ring-1 ring-cyan-200/60",
    shouldBlink ? "animate-storyboard-inline-blink" : "animate-storyboard-inline-pulse",
  ];
}

function codeBlockCueClass(block) {
  if (props.activeCue?.dynamicGuidance?.primaryEffect !== "code-highlight") return "border-white/10";
  const fields = activeCodeFields.value;
  if (!fields.length || fields.some((field) => block.code?.includes(field))) {
    return "border-emerald-300/70 shadow-lg shadow-emerald-500/20 animate-storyboard-block-pulse";
  }
  return "border-white/10";
}

function splitCodeLine(line) {
  const fields = activeCodeFields.value;
  if (!fields.length) return [{ text: line }];
  const pattern = new RegExp(`(${fields.map(escapeRegExp).join("|")})`, "g");
  return line.split(pattern).filter(Boolean).map((text) => ({ text }));
}

function codeLines(block) {
  return (block.code || "").split("\n");
}

function codeFieldCueClass(text) {
  if (!activeCodeFields.value.includes(text)) return "";
  const shouldBlink = props.activeCue?.dynamicGuidance?.visualTreatment?.blink;
  return [
    "rounded bg-emerald-300/20 px-1 text-emerald-50 shadow-lg shadow-emerald-500/25 ring-1 ring-emerald-200/60",
    shouldBlink ? "animate-storyboard-inline-blink" : "animate-storyboard-inline-pulse",
  ];
}

function escapeRegExp(text) {
  const specialChars = new Set(["\\", "^", "$", ".", "*", "+", "?", "(", ")", "[", "]", "{", "}", "|"]);
  return text
    .split("")
    .map((char) => (specialChars.has(char) ? `\\${char}` : char))
    .join("");
}

// activeVisualSpec → CSS 自定义属性，驱动动画
const activeVisualSpecStyle = computed(() => {
  const spec = activeVisualSpec.value;
  if (!spec) return {};
  const p = spec.animation?.parameters || {};
  const visual = spec.dynamicGuidance?.visualTreatment || {};
  return {
    "--viz-opacity-start": p.opacity?.[0] ?? 0,
    "--viz-opacity-end": p.opacity?.[1] ?? 1,
    "--viz-translate-y-start": (p.translateY?.[0] ?? 12) + "px",
    "--viz-translate-y-end": (p.translateY?.[1] ?? 0) + "px",
    "--viz-duration": (spec.animation?.durationMs ?? 400) + "ms",
    "--viz-easing": spec.animation?.easing ?? "ease-out",
    "--viz-accent": visual.accent === "cyan" ? "#67e8f9" : "#6ee7b7",
    "--viz-glow": visual.glow ? "0 0 18px 2px rgba(103,232,249,.35)" : "none",
  };
});

// 当 activeVisualSpec 变化时，给目标元素添加动画 class
watch(() => activeVisualSpec.value, (spec, oldSpec) => {
  if (!spec) return;
  // 移除旧的高亮
  document.querySelectorAll("[data-visual-active]").forEach(el => el.removeAttribute("data-visual-active"));
  // 给目标 point-card 加上视觉激活标记
  const target = spec.dynamicGuidance?.highlightTarget || "point-card";
  const label = spec.knowledgeFocus?.label || spec.contentBeat || "";
  document.querySelectorAll(".point-card").forEach(el => {
    const text = el.textContent || "";
    if (label && text.includes(label.slice(0, 8))) {
      el.setAttribute("data-visual-active", "true");
    }
  });
});

</script>
<style scoped>
/* === visualSpecs 驱动的表演动画 === */

/* reveal-focus：从透明+下移 淡入归位 */
@keyframes reveal-focus {
  0% {
    opacity: 0;
    transform: translateY(12px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.point-card {
  transition: opacity 0.4s ease-out, transform 0.4s ease-out,
              box-shadow 0.4s ease-out, border-color 0.4s ease-out;
}

.point-card[data-visual-active="true"] {
  animation: reveal-focus v-bind(animDuration) v-bind(animEasing);
  animation-fill-mode: both;
  border-color: rgba(103, 232, 249, 0.5);
  box-shadow: 0 0 18px 2px rgba(103, 232, 249, 0.25);
}

.point-card:not([data-visual-active]) {
  opacity: 0.82;
}
</style>

