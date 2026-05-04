<template>

  <main class="min-h-screen touch-pan-y bg-neutral-950 text-white" @click="handleSurfaceClick" @touchstart.passive="handleTouchStart" @touchend.passive="handleTouchEnd">

    <div class="grid min-h-screen grid-rows-[auto_1fr_auto_auto]">

      <section class="px-4 pt-4 lg:px-6">

        <BreadcrumbNav :module-id="slide.moduleId" :slide-id="slide.slideId" class="mx-auto max-w-7xl text-white/70" />

      </section>

      <section class="p-4 lg:p-6">

        <SlideCanvas

          :slide="slide"

          :active-cue="activeCue"

          :composition="visualComposition"

          :motion-cues="motionCues"

          :visual-specs="visualSpecs"

          :performance-specs="performanceSpecs"

          :current-time="currentTime"

          class="mx-auto max-w-7xl"

        />

      </section>

      <section class="px-4 pb-4 lg:px-6">

        <SubtitleOverlay :text="currentSubtitle" class="mx-auto max-w-7xl" />

      </section>

      <SlideNav

        ref="slideNav"

        :slide="slide"

        :module-slides="moduleSlides"

        @subtitle-change="currentSubtitle = $event"

        @subtitle-index-change="handleSubtitleIndexChange"

        @time-update="currentTime = $event"

      />

    </div>

  </main>

</template>

<script setup>

import { computed, ref, watch } from "vue";

import BreadcrumbNav from "./BreadcrumbNav.vue";

import SlideCanvas from "./SlideCanvas.vue";

import SlideNav from "./SlideNav.vue";

import SubtitleOverlay from "./SubtitleOverlay.vue";

import storyboardContract from "../data/storyboard-contract.json";



const props = defineProps({ slide: { type: Object, required: true }, moduleSlides: { type: Array, required: true } });

const currentSubtitle = ref("");

const currentTime = ref(0);

const slideNav = ref(null);

const touchStartY = ref(0);

const touchStartX = ref(0);

const revealedCueIds = ref([]);

const storyboardSlide = computed(() =>

  (storyboardContract.slides || []).find((item) => item.moduleId === props.slide.moduleId && item.slideId === props.slide.slideId),

);

const motionCues = computed(() => storyboardSlide.value?.motionCues ?? []);

const visualComposition = computed(() => storyboardSlide.value?.visualComposition ?? null);

const activeCue = computed(() => {

  const byTime = motionCues.value.find((cue) => {

    const start = Number(cue.timeRange?.start ?? cue.dynamicGuidance?.timing?.start ?? cue.trigger?.start ?? NaN);

    const end = Number(cue.timeRange?.end ?? cue.dynamicGuidance?.timing?.settle ?? cue.trigger?.end ?? NaN);

    return Number.isFinite(start) && Number.isFinite(end) && currentTime.value >= start && currentTime.value < end;

  });

  if (byTime) return byTime;

  return motionCues.value.find((cue) => revealedCueIds.value.includes(cue.cueId)) ?? null;

});



function handleSubtitleIndexChange(index) {

  if (index < 0) return;

  const nextCueIds = motionCues.value

    .filter((cue) => Number(cue.trigger?.segmentIndex) <= index)

    .map((cue) => cue.cueId);

  revealedCueIds.value = [...new Set([...revealedCueIds.value, ...nextCueIds])];

}

watch(() => props.slide.slideId, () => {

  revealedCueIds.value = [];

  currentSubtitle.value = "";

  currentTime.value = 0;

});

function handleSurfaceClick(event) {

  if (event.target.closest("button,a,input,footer,nav")) return;

  slideNav.value?.toggle();

}

function handleTouchStart(event) {

  const touch = event.changedTouches[0];

  touchStartY.value = touch.clientY;

  touchStartX.value = touch.clientX;

}

function handleTouchEnd(event) {

  const touch = event.changedTouches[0];

  const deltaY = touch.clientY - touchStartY.value;

  const deltaX = touch.clientX - touchStartX.value;

  if (Math.abs(deltaY) < 56 || Math.abs(deltaY) < Math.abs(deltaX) * 1.2) return;

  if (deltaY < 0) slideNav.value?.goNext();

  else slideNav.value?.goPrev();

}

</script>

