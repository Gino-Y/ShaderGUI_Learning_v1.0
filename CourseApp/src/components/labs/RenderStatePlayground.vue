<template>
  <article class="grid gap-4 rounded-lg border border-white/10 bg-white/[0.04] p-5 lg:grid-cols-[0.9fr_1.1fr]">
    <section class="grid gap-3">
      <button
        v-for="scenario in scenarios"
        :key="scenario.id"
        class="rounded-md border px-4 py-3 text-left transition"
        :class="scenario.id === activeScenario ? 'border-emerald-300 bg-emerald-300/15' : 'border-white/10 bg-neutral-900'"
        type="button"
        @click="activeScenario = scenario.id"
      >
        <span class="block text-sm font-semibold text-emerald-200">{{ scenario.name }}</span>
        <span class="mt-1 block text-white/65">{{ scenario.intent }}</span>
      </button>
    </section>
    <section class="rounded-md border border-white/10 bg-neutral-900 p-5">
      <p class="text-sm font-semibold text-white/50">渲染状态</p>
      <h2 class="mt-2 text-2xl font-semibold">{{ current.name }}</h2>
      <div class="mt-5 grid gap-3">
        <label v-for="item in current.params" :key="item.label" class="grid gap-2">
          <span class="text-sm text-white/70">{{ item.label }}</span>
          <input v-if="item.type === 'range'" class="accent-emerald-400" type="range" min="0" max="100" :value="item.seed" />
          <label v-else-if="item.type === 'toggle'" class="flex items-center gap-2">
            <input class="accent-emerald-400" type="checkbox" :checked="item.defaultOn" />
            <span class="text-sm text-white/60">{{ item.defaultOn ? 'On' : 'Off' }}</span>
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
const scenarios = [
  { id: "transparent", name: "透明物体", intent: "Alpha Blend + 关闭深度写入的标准透明设置。", params: [{ label: "Alpha Cutoff", type: "range", seed: 30 }, { label: "ZWrite", type: "toggle", defaultOn: false }, { label: "RenderQueue", type: "range", seed: 75 }], takeaway: "透明物体必须关闭 ZWrite，否则会被自身遮挡；Queue 须设为 Transparent。" },
  { id: "cutout", name: "镂空材质", intent: "Alpha Test 模式，保留深度写入但丢弃低于阈值的片元。", params: [{ label: "Alpha Cutoff", type: "range", seed: 50 }, { label: "ZWrite", type: "toggle", defaultOn: true }, { label: "RenderQueue", type: "range", seed: 45 }], takeaway: "镂空材质保留 ZWrite，所以渲染顺序不敏感，适合植被和细节纹理。" },
  { id: "additive", name: "叠加光效", intent: "Additive 混合模式，常用于火焰、粒子、光晕。", params: [{ label: "Intensity", type: "range", seed: 80 }, { label: "ZWrite", type: "toggle", defaultOn: false }, { label: "BlendOp", type: "toggle", defaultOn: true }], takeaway: "Additive 把源色叠加到目标上，不修改 Alpha，适合发光效果。" },
];
const activeScenario = ref(scenarios[0].id);
const current = computed(() => scenarios.find((s) => s.id === activeScenario.value) || scenarios[0]);
</script>
