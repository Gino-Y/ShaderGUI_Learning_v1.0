<template>
  <main class="min-h-screen bg-neutral-950 px-4 py-6 text-white sm:px-8">
    <section class="mx-auto max-w-6xl">
      <BreadcrumbNav :items="[{ label: '课程首页' }]" />
      <div class="rounded-[2rem] border border-white/10 bg-white/[0.04] p-6 shadow-2xl shadow-cyan-950/30 sm:p-8">
        <p class="text-sm font-semibold uppercase tracking-[0.24em] text-emerald-300">Course</p>
        <h1 class="mt-4 text-4xl font-semibold tracking-tight sm:text-5xl">{{ course.title }}</h1>
        <p class="mt-4 max-w-3xl text-lg leading-8 text-slate-300">{{ course.subtitle }}</p>
      </div>

      <div class="mt-6 grid gap-5">
        <section
          v-for="module in course.modules"
          :key="module.id"
          class="rounded-[1.5rem] border border-white/10 bg-slate-900/80 p-5"
        >
          <div class="sm:hidden">
            <div>
              <p class="text-xs font-semibold uppercase tracking-[0.22em] text-cyan-300">{{ module.id }}</p>
              <h2 class="mt-2 text-2xl font-semibold">{{ module.title }}</h2>
              <p class="mt-2 max-w-3xl text-sm leading-6 text-slate-300">{{ module.summary }}</p>
            </div>

            <div class="mt-4">
              <p class="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">学习状态</p>
              <div class="mt-2 grid grid-cols-2 gap-2" :aria-label="`${module.title} 学习状态`">
                <button
                  v-for="step in progressSteps"
                  :key="step.key"
                  type="button"
                  :aria-pressed="isStepReached(module.id, step.level)"
                  :class="progressButtonClass(module.id, step.level)"
                  @click="setModuleProgress(module.id, step.level)"
                >
                  {{ step.label }}
                </button>
              </div>
            </div>

            <RouterLink
              :to="`/module/${module.id}/quiz`"
              class="mt-4 block w-full rounded-xl border border-emerald-300/40 bg-emerald-300/10 px-4 py-2 text-center text-sm font-semibold text-emerald-100 transition hover:bg-emerald-300/20"
            >
              进入做题页
            </RouterLink>
            <div class="mt-5 grid gap-3">
              <div
                v-for="slide in slidesForModule(module.id)"
                :key="`m-${slide.slideId}`"
                class="rounded-2xl border border-white/10 bg-white/[0.04] p-4"
              >
                <div class="grid grid-cols-1 gap-3">
                  <span class="text-sm font-semibold text-slate-400">{{ slide.slideId }}</span>
                  <RouterLink :to="slide.route" class="font-semibold text-white transition hover:text-cyan-200">
                    {{ slide.title }}
                  </RouterLink>
                  <RouterLink :to="slide.route" class="text-sm font-semibold text-cyan-200 transition hover:text-cyan-100">
                    开始
                  </RouterLink>
                  <RouterLink
                    v-if="slide.explore"
                    :to="slide.explore.route"
                    class="rounded-xl border border-emerald-300/40 bg-emerald-300/10 px-3 py-2 text-center text-xs font-semibold text-emerald-100 transition hover:bg-emerald-300/20"
                  >
                    探索
                  </RouterLink>
                </div>
              </div>
            </div>
          </div>

          <div class="hidden gap-x-3 gap-y-4 sm:grid sm:grid-cols-[2.75rem_minmax(0,1fr)_5rem_8rem]">
            <div class="min-w-0 sm:col-span-3 sm:pb-1">
              <p class="text-xs font-semibold uppercase tracking-[0.22em] text-cyan-300">{{ module.id }}</p>
              <h2 class="mt-2 text-2xl font-semibold">{{ module.title }}</h2>
              <p class="mt-2 max-w-3xl text-sm leading-6 text-slate-300">{{ module.summary }}</p>
            </div>
            <RouterLink
              :to="`/module/${module.id}/quiz`"
              class="w-full self-center rounded-xl border border-emerald-300/40 bg-emerald-300/10 px-3 py-2 text-center text-xs font-semibold text-emerald-100 transition hover:bg-emerald-300/20 sm:px-4 sm:text-sm"
            >
              进入做题页
            </RouterLink>

            <div class="col-span-4 grid gap-2 rounded-xl border border-white/10 bg-white/[0.03] p-3 md:grid-cols-[5rem_1fr] md:items-center">
              <p class="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">学习状态</p>
              <div class="grid grid-cols-4 gap-2" :aria-label="`${module.title} 学习状态`">
                <button
                  v-for="step in progressSteps"
                  :key="step.key"
                  type="button"
                  :aria-pressed="isStepReached(module.id, step.level)"
                  :class="progressButtonClass(module.id, step.level)"
                  @click="setModuleProgress(module.id, step.level)"
                >
                  {{ step.label }}
                </button>
              </div>
            </div>

            <template v-for="(slide, idx) in slidesForModule(module.id)" :key="slide.slideId">
              <hr v-if="idx > 0" class="col-span-4 m-0 h-0 border-0 border-t border-white/15" />
              <div class="flex items-start pt-1 text-sm font-semibold text-slate-400">{{ slide.slideId }}</div>
              <RouterLink
                :to="slide.route"
                class="min-w-0 break-words py-1.5 font-semibold text-white transition hover:text-cyan-200"
              >
                {{ slide.title }}
              </RouterLink>
              <RouterLink
                :to="slide.route"
                class="py-1.5 text-center text-sm font-semibold text-cyan-200 transition hover:text-cyan-100"
              >
                开始
              </RouterLink>
              <div
                :class="[
                  'flex min-h-[2.75rem] items-center justify-center',
                  slide.explore ? '' : 'invisible pointer-events-none',
                ]"
              >
                <RouterLink
                  v-if="slide.explore"
                  :to="slide.explore.route"
                  class="w-full rounded-xl border border-emerald-300/40 bg-emerald-300/10 px-3 py-2 text-center text-xs font-semibold text-emerald-100 transition hover:bg-emerald-300/20 sm:px-4 sm:text-sm"
                >
                  探索
                </RouterLink>
              </div>
            </template>
          </div>
        </section>
      </div>
    </section>
  </main>
</template>
<script setup>
import { onMounted, ref, watch } from "vue";
import BreadcrumbNav from "../components/BreadcrumbNav.vue";
import course from "../data/course.json";
import slides from "../data/slides.json";

const STORAGE_KEY = "shadergui-module-progress-v1";
const progressSteps = [
  { key: "watched", label: "看过", level: 1 },
  { key: "learned", label: "学过", level: 2 },
  { key: "practiced", label: "已做题", level: 3 },
  { key: "mastered", label: "掌握", level: 4 },
];
const moduleProgress = ref({});

function slidesForModule(moduleId) {
  return slides.filter((slide) => slide.moduleId === moduleId).sort((a, b) => a.order - b.order);
}

function isStepReached(moduleId, level) {
  return Number(moduleProgress.value[moduleId] || 0) >= level;
}

function progressButtonClass(moduleId, level) {
  const base =
    "min-h-10 rounded-md border px-2 text-sm font-semibold transition focus:outline-none focus:ring-2 focus:ring-cyan-200/70";
  if (isStepReached(moduleId, level)) {
    return `${base} border-emerald-300/70 bg-emerald-300/20 text-emerald-50`;
  }
  return `${base} border-white/10 bg-slate-950/40 text-slate-300 hover:border-cyan-300/60 hover:text-cyan-100`;
}

function setModuleProgress(moduleId, level) {
  const current = Number(moduleProgress.value[moduleId] || 0);
  moduleProgress.value = {
    ...moduleProgress.value,
    [moduleId]: current === level ? Math.max(0, level - 1) : level,
  };
}

onMounted(() => {
  try {
    const saved = JSON.parse(window.localStorage.getItem(STORAGE_KEY) || "{}");
    moduleProgress.value = Object.fromEntries(
      Object.entries(saved).map(([moduleId, level]) => [moduleId, Math.min(4, Math.max(0, Number(level) || 0))]),
    );
  } catch {
    moduleProgress.value = {};
  }
});

watch(
  moduleProgress,
  (value) => {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(value));
  },
  { deep: true },
);
</script>
