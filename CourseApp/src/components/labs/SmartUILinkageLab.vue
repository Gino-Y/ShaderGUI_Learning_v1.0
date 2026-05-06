<template>
  <article class="grid gap-4 rounded-lg border border-white/10 bg-white/[0.04] p-5 lg:grid-cols-[0.9fr_1.1fr]">
    <section class="grid gap-3">
      <button
        v-for="control in controls"
        :key="control.id"
        class="rounded-md border px-4 py-3 text-left transition"
        :class="control.id === activeControl ? 'border-emerald-300 bg-emerald-300/15' : 'border-white/10 bg-neutral-900'"
        type="button"
        @click="activeControl = control.id"
      >
        <span class="block text-sm font-semibold text-emerald-200">{{ control.name }}</span>
        <span class="mt-1 block text-white/65">{{ control.intent }}</span>
      </button>
    </section>
    <section class="rounded-md border border-white/10 bg-neutral-900 p-5">
      <p class="text-sm font-semibold text-white/50">控制类型</p>
      <h2 class="mt-2 text-2xl font-semibold">{{ current.name }}</h2>
      <div class="mt-5 grid gap-3">
        <label v-for="item in current.params" :key="item.label" class="grid gap-2">
          <span class="text-sm text-white/70">{{ item.label }}</span>
          <input v-if="item.type === 'range'" class="accent-emerald-400" type="range" min="0" max="100" :value="item.seed" />
          <select v-else-if="item.type === 'enum'" class="rounded border border-white/15 bg-neutral-800 px-3 py-1.5 text-sm text-white">
            <option v-for="opt in item.options" :key="opt">{{ opt }}</option>
          </select>
          <label v-else-if="item.type === 'toggle'" class="flex items-center gap-2">
            <input class="accent-emerald-400" type="checkbox" :checked="item.defaultOn" />
            <span class="text-sm text-white/60">{{ item.defaultOn ? '已启用' : '已关闭' }}</span>
          </label>
        </label>
      </div>
      <p class="mt-5 rounded-md bg-emerald-300/10 px-4 py-3 text-emerald-100">{{ current.takeaway }}</p>
    </section>
  </article>
</template>
<script setup>
import { computed, ref } from "vue";

defineProps({ slide: { type: Object, required: true }, exploration: { type: Object, required: true } });
const controls = [
  { id: "toggle", name: "Toggle 开关", intent: "布尔状态切换，最基础的控制类型。", params: [{ label: "启用特效", type: "toggle", defaultOn: true }, { label: "Debug 模式", type: "toggle", defaultOn: false }], takeaway: "Toggle 把 true/false 映射为开关 UI，让材质参数在 Inspector 里一键切换。" },
  { id: "enum", name: "Enum 下拉", intent: "多选一，适合有限集合的场景。", params: [{ label: "混合模式", type: "enum", options: ["Opaque", "Alpha Blend", "Additive", "Premultiply"] }, { label: "渲染队列", type: "enum", options: ["Background", "Geometry", "Transparent", "Overlay"] }], takeaway: "Enum 把整数值映射为可读标签，避免用户记忆魔法数字。" },
  { id: "linkage", name: "联动逻辑", intent: "一个控件的变更驱动其他参数自动更新。", params: [{ label: "混合模式", type: "enum", options: ["Opaque", "Alpha Blend"] }, { label: "渲染队列（自动联动）", type: "enum", options: ["Geometry", "Transparent"] }, { label: "深度写入（自动联动）", type: "toggle", defaultOn: true }], takeaway: "联动让用户只改一个值，系统自动推导依赖参数，减少不一致风险。" },
];
const activeControl = ref(controls[0].id);
const current = computed(() => controls.find((c) => c.id === activeControl.value) || controls[0]);
</script>
