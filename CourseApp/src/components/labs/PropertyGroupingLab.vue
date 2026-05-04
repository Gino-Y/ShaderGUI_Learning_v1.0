<template>
  <article class="grid gap-4 rounded-lg border border-white/10 bg-white/[0.04] p-5 lg:grid-cols-[0.9fr_1.1fr]">
    <section class="grid gap-3">
      <button
        v-for="group in groups"
        :key="group.id"
        class="rounded-md border px-4 py-3 text-left transition"
        :class="group.id === activeGroup ? 'border-emerald-300 bg-emerald-300/15' : 'border-white/10 bg-neutral-900'"
        type="button"
        @click="activeGroup = group.id"
      >
        <span class="block text-sm font-semibold text-emerald-200">{{ group.name }}</span>
        <span class="mt-1 block text-white/65">{{ group.intent }}</span>
      </button>
    </section>
    <section class="rounded-md border border-white/10 bg-neutral-900 p-5">
      <p class="text-sm font-semibold text-white/50">当前调参视图</p>
      <h2 class="mt-2 text-2xl font-semibold">{{ active.name }}</h2>
      <div class="mt-5 grid gap-3">
        <label v-for="item in active.params" :key="item" class="grid gap-2">
          <span class="text-sm text-white/70">{{ item }}</span>
          <input class="accent-emerald-400" type="range" min="0" max="100" :value="active.seed" />
        </label>
      </div>
      <p class="mt-5 rounded-md bg-emerald-300/10 px-4 py-3 text-emerald-100">{{ active.takeaway }}</p>
    </section>
  </article>
</template>
<script setup>
import { computed, ref } from "vue";

defineProps({ slide: { type: Object, required: true }, exploration: { type: Object, required: true } });
const groups = [
  { id: "surface", name: "表面表现", intent: "优先暴露美术最常改的视觉参数。", seed: 62, params: ["Base Color", "Roughness", "Metallic"], takeaway: "高频参数聚在一起，减少寻找成本。" },
  { id: "render", name: "渲染状态", intent: "把 Blend、ZWrite、Queue 放进受控区域。", seed: 38, params: ["Blend", "ZWrite", "RenderQueue"], takeaway: "状态类参数集中管理，降低误配风险。" },
  { id: "advanced", name: "高级开关", intent: "低频项默认收起，只在需要时展开。", seed: 20, params: ["Debug Mode", "Keyword", "Override"], takeaway: "渐进式揭露让界面服务任务，而不是堆满信息。" },
];
const activeGroup = ref(groups[0].id);
const active = computed(() => groups.find((group) => group.id === activeGroup.value) || groups[0]);
</script>
