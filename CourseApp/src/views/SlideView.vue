<template>
  <CoursePlayer v-if="slide" :slide="slide" :module-slides="moduleSlides" />
  <main v-else class="grid min-h-screen place-items-center">
    <RouterLink to="/" class="text-emerald-700">返回课程首页</RouterLink>
  </main>
</template>
<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import CoursePlayer from "../components/CoursePlayer.vue";
import slides from "../data/slides.json";

const route = useRoute();
const slide = computed(() =>
  slides.find((item) => item.moduleId === route.params.moduleId && item.slideId === route.params.slideId),
);
const moduleSlides = computed(() =>
  slides.filter((item) => item.moduleId === route.params.moduleId).sort((a, b) => a.order - b.order),
);
</script>
