<template>
  <main class="min-h-screen bg-[#f5f5f2] px-6 py-8 text-neutral-950 sm:px-10">
    <section class="mx-auto max-w-5xl">
      <BreadcrumbNav :module-id="String(route.params.moduleId)" label="模块目录" />
      <h1 class="mt-6 text-4xl font-semibold tracking-normal">{{ module?.title }}</h1>
      <p class="mt-3 max-w-3xl text-neutral-600">{{ module?.summary }}</p>
      <div class="mt-8 grid gap-3 rounded-lg border border-neutral-200 bg-white p-5 shadow-sm">
        <RouterLink
          v-for="slide in moduleSlides"
          :key="slide.slideId"
          :to="slide.route"
          class="grid gap-3 rounded-md border border-neutral-200 px-5 py-4 transition hover:border-emerald-600 sm:grid-cols-[auto_1fr_auto]"
        >
          <span class="text-neutral-500">{{ slide.slideId }}</span>
          <span class="font-medium text-neutral-950">{{ slide.title }}</span>
          <span class="font-medium text-emerald-700">进入</span>
          <RouterLink
            v-if="slide.explore"
            :to="slide.explore.route"
            class="sm:col-start-2 w-fit rounded-md border border-emerald-200 bg-emerald-50 px-3 py-1 text-sm font-medium text-emerald-800"
            @click.stop
          >
            探索
          </RouterLink>
        </RouterLink>
        <RouterLink :to="`/module/${route.params.moduleId}/quiz`" class="flex items-center justify-between rounded-md border border-emerald-500 bg-emerald-50 px-5 py-4 hover:bg-emerald-100">
          <span class="font-medium text-neutral-950">做题页</span>
          <span class="font-medium text-emerald-700">开始</span>
        </RouterLink>
      </div>
    </section>
  </main>
</template>
<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import BreadcrumbNav from "../components/BreadcrumbNav.vue";
import course from "../data/course.json";
import slides from "../data/slides.json";

const route = useRoute();
const module = computed(() => course.modules.find((item) => item.id === route.params.moduleId));
const moduleSlides = computed(() =>
  slides.filter((slide) => slide.moduleId === route.params.moduleId).sort((a, b) => a.order - b.order),
);
</script>
