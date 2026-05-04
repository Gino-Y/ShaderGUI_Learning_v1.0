<template>
  <nav class="mb-3 text-xs text-slate-400" aria-label="面包屑导航">
    <ol class="flex flex-wrap items-center gap-1.5">
      <li v-for="(item, index) in resolvedItems" :key="`${item.label}-${index}`" class="inline-flex items-center gap-1.5">
        <RouterLink
          v-if="item.to && index < resolvedItems.length - 1"
          :to="item.to"
          class="transition hover:text-slate-100"
        >
          {{ item.label }}
        </RouterLink>
        <span v-else class="text-slate-300">{{ item.label }}</span>
        <span v-if="index < resolvedItems.length - 1" class="text-slate-600" aria-hidden="true">/</span>
      </li>
    </ol>
  </nav>
</template>
<script setup>
import { computed } from "vue";

const props = defineProps({
  items: { type: Array, default: null },
  moduleId: { type: String, default: "" },
  slideId: { type: String, default: "" },
  label: { type: String, default: "" },
});

const resolvedItems = computed(() => {
  if (props.items?.length) return props.items;
  const items = [{ label: "课程首页", to: "/" }];
  if (props.moduleId) items.push({ label: props.moduleId, to: "/" });
  if (props.slideId) items.push({ label: props.slideId, to: `/module/${props.moduleId}/slide/${props.slideId}` });
  if (props.label) items.push({ label: props.label });
  return items;
});
</script>
