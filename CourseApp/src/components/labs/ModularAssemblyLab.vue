<template>
  <article class="grid gap-4 rounded-lg border border-white/10 bg-white/[0.04] p-5 lg:grid-cols-[0.9fr_1.1fr]">
    <section class="grid gap-3">
      <button
        v-for="mod in modules"
        :key="mod.id"
        class="rounded-md border px-4 py-3 text-left transition"
        :class="mod.id === activeMod ? 'border-emerald-300 bg-emerald-300/15' : 'border-white/10 bg-neutral-900'"
        type="button"
        @click="activeMod = mod.id"
      >
        <span class="block text-sm font-semibold text-emerald-200">{{ mod.name }}</span>
        <span class="mt-1 block text-white/65">{{ mod.intent }}</span>
      </button>
    </section>
    <section class="rounded-md border border-white/10 bg-neutral-900 p-5">
      <p class="text-sm font-semibold text-white/50">当前模块</p>
      <h2 class="mt-2 text-2xl font-semibold">{{ current.name }}</h2>
      <div class="mt-5 grid gap-3">
        <label v-for="item in current.props" :key="item" class="grid gap-2">
          <span class="text-sm text-white/70">{{ item }}</span>
          <input class="accent-emerald-400" type="range" min="0" max="100" :value="current.seed" />
        </label>
      </div>
      <p class="mt-5 rounded-md bg-emerald-300/10 px-4 py-3 text-emerald-100">{{ current.takeaway }}</p>
    </section>
  </article>
</template>
<script setup>
import { computed, ref } from "vue";

defineProps({ slide: { type: Object, required: true }, exploration: { type: Object, required: true } });
const modules = [
  { id: "basecolor", name: "BaseColorModule", intent: "基础颜色模块，管理 Albedo 和色调映射。", seed: 70, props: ["Base Color", "Hue Shift", "Saturation"], takeaway: "每个 Module 只管一个职责。BaseColorModule 只关心颜色，不管渲染状态。" },
  { id: "renderstate", name: "RenderStateModule", intent: "渲染状态模块，管理 Blend / ZWrite / Queue。", seed: 45, props: ["Blend Mode", "ZWrite", "RenderQueue"], takeaway: "渲染状态从业务逻辑中分离，便于跨 Shader 复用状态配置。" },
  { id: "assembled", name: "组装结果", intent: "多个 Module 通过 Assembly 组合为完整 ShaderGUI。", seed: 85, props: ["Base Color", "Roughness", "Blend Mode", "ZWrite"], takeaway: "Module 化设计让 ShaderGUI 像搭积木一样组合，每个模块独立可测试。" },
];
const activeMod = ref(modules[0].id);
const current = computed(() => modules.find((m) => m.id === activeMod.value) || modules[0]);
</script>
