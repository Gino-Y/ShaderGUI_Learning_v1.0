<template>
  <main class="min-h-screen bg-neutral-950 px-4 py-5 text-white sm:px-8">
    <section v-if="slide && exploration" class="mx-auto grid max-w-6xl gap-5">
      <BreadcrumbNav :module-id="moduleId" :slide-id="slideId" label="探索页" class="text-white" />
      <header class="rounded-lg border border-white/10 bg-white/[0.04] p-5">
        <p class="text-sm font-semibold text-emerald-300">{{ slideId }} 的子页面</p>
        <h1 class="mt-2 text-3xl font-semibold tracking-normal">{{ exploration.title }}</h1>
        <p class="mt-2 text-white/65">{{ slide.title }}</p>
      </header>
      <component :is="labComponent" v-if="labComponent" :slide="slide" :exploration="exploration" />
      <article v-else class="rounded-lg border border-white/10 bg-white/[0.04] p-5">
        <p class="text-white/70">探索组件未找到。</p>
      </article>
      <div class="flex flex-wrap gap-3">
        <RouterLink :to="slide.route" class="rounded-md bg-emerald-500 px-4 py-2 font-semibold text-neutral-950">回到当前课</RouterLink>
        <RouterLink to="/" class="rounded-md border border-white/15 px-4 py-2 font-medium">回到菜单</RouterLink>
        <RouterLink :to="`/module/${moduleId}/quiz`" class="rounded-md border border-white/15 px-4 py-2 font-medium">去做题</RouterLink>
      </div>
    </section>
  </main>
</template>
<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import BreadcrumbNav from "../components/BreadcrumbNav.vue";
import slides from "../data/slides.json";
import explorations from "../data/explorations.json";
import PropertyGroupingLab from "../components/labs/PropertyGroupingLab.vue";

const labs = { PropertyGroupingLab };
const route = useRoute();
const moduleId = computed(() => String(route.params.moduleId));
const slideId = computed(() => String(route.params.slideId));
const slide = computed(() => slides.find((item) => item.moduleId === moduleId.value && item.slideId === slideId.value));
const exploration = computed(() =>
  explorations.find((item) => item.moduleId === moduleId.value && item.parentSlideId === slideId.value)
  ?? slide.value?.explore
  ?? null,
);
const labComponent = computed(() => labs[exploration.value?.component]);
</script>
