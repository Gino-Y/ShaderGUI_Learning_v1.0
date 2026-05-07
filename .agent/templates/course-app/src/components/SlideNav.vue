<template>
  <footer class="border-t border-white/10 bg-neutral-950/95 px-4 py-3 backdrop-blur" @click.stop>
    <div class="mx-auto grid max-w-7xl gap-3">
      <div class="flex items-center gap-3">
        <button
          class="grid h-10 w-10 shrink-0 place-items-center rounded-full bg-emerald-400 text-neutral-950 transition hover:bg-emerald-300"
          type="button"
          :aria-label="playing ? '暂停' : '播放'"
          @click="toggle"
        >
          <svg v-if="playing" class="h-5 w-5" viewBox="0 0 24 24" aria-hidden="true" data-player-icon="pause">
            <rect x="7" y="5" width="3.75" height="14" rx="1.25" fill="currentColor" />
            <rect x="13.25" y="5" width="3.75" height="14" rx="1.25" fill="currentColor" />
          </svg>
          <svg v-else class="h-5 w-5 translate-x-0.5" viewBox="0 0 24 24" aria-hidden="true" data-player-icon="play">
            <path d="M8 5.75v12.5L17.5 12 8 5.75z" fill="currentColor" />
          </svg>
        </button>
        <input v-model.number="seekPercent" class="h-2 w-full cursor-pointer accent-emerald-400" type="range" min="0" max="100" step="0.1" aria-label="音频进度" @pointerdown="beginSeek" @pointerup="endSeek" @touchstart="beginSeek" @touchend="endSeek" @change="endSeek" />
      </div>
      <div class="grid gap-3 sm:grid-cols-[1fr_auto_1fr] sm:items-center">
        <div class="flex flex-wrap items-center gap-2 sm:justify-start">
          <RouterLink to="/" class="rounded-md border border-white/15 px-3 py-2 text-sm text-white/80 transition hover:border-cyan-300/50 hover:text-white">目录</RouterLink>
          <RouterLink v-if="slide.explore" :to="slide.explore.route" class="rounded-md border border-emerald-400/60 px-3 py-2 text-sm text-emerald-200 transition hover:bg-emerald-400/10">探索</RouterLink>
        </div>
        <div class="min-w-0 text-left sm:text-center">
          <p class="truncate text-sm text-white/80">{{ slide.title }}</p>
          <p class="text-xs text-white/45">{{ formatTime(currentTime) }} / {{ formatTime(duration) }}</p>
        </div>
        <div class="flex flex-wrap items-center gap-2 sm:justify-end">
          <RouterLink :to="prevRoute || '#'" class="rounded-md border border-white/15 px-3 py-2 text-sm text-white/80 transition hover:border-cyan-300/50 hover:text-white" :class="{ 'pointer-events-none opacity-40': !prevRoute }">上一页</RouterLink>
          <RouterLink :to="nextRoute" class="rounded-md border border-white/15 px-3 py-2 text-sm text-white/80 transition hover:border-cyan-300/50 hover:text-white">{{ nextLabel }}</RouterLink>
        </div>
      </div>
      <audio ref="audio" :src="resolvedAudioSrc" class="hidden" preload="auto" playsinline @loadedmetadata="syncDuration" @canplay="requestInitialPlayback" @play="playing = true" @pause="playing = false" @timeupdate="syncPlayback" @ended="handleEnded" />
    </div>
  </footer>
</template>
<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";

const props = defineProps({ slide: { type: Object, required: true }, moduleSlides: { type: Array, required: true } });
const emit = defineEmits(["subtitle-change", "subtitle-index-change", "time-update"]);
const router = useRouter();
const audio = ref(null);
const playing = ref(false);
const currentTime = ref(0);
const duration = ref(0);
const seeking = ref(false);
const resumeAfterSeek = ref(true);
const initialPlayRequested = ref(false);
const subtitleEvents = ref([]);
const currentIndex = computed(() => props.moduleSlides.findIndex((item) => item.slideId === props.slide.slideId));
const prevRoute = computed(() => props.moduleSlides[currentIndex.value - 1]?.route ?? "");
const isLastSlide = computed(() => currentIndex.value === props.moduleSlides.length - 1);
const nextRoute = computed(() => props.moduleSlides[currentIndex.value + 1]?.route ?? `/module/${props.slide.moduleId}/quiz`);
const nextLabel = computed(() => (isLastSlide.value ? "做题页" : "下一页"));
const resolvedAudioSrc = computed(() => resolvePublicAsset(props.slide.audio));
const seekPercent = computed({
  get() {
    if (!duration.value) return 0;
    return Math.min(100, Math.max(0, (currentTime.value / duration.value) * 100));
  },
  set(value) {
    if (!audio.value || !duration.value) return;
    const nextTime = (Number(value) / 100) * duration.value;
    audio.value.currentTime = nextTime;
    currentTime.value = nextTime;
    emit("time-update", currentTime.value);
    syncSubtitle();
  },
});
function emitSubtitle(text) { emit("subtitle-change", text); }
async function playCurrent() {
  if (!audio.value) return;
  try { await audio.value.play(); } catch { playing.value = false; }
}
function requestInitialPlayback() {
  if (initialPlayRequested.value) return;
  initialPlayRequested.value = true;
  playCurrent();
}
function toggle() {
  if (!audio.value) return;
  if (audio.value.paused) playCurrent();
  else audio.value.pause();
}
function goNext() { if (nextRoute.value) router.push(nextRoute.value); }
function goPrev() { if (prevRoute.value) router.push(prevRoute.value); }
async function loadSubtitles() {
  subtitleEvents.value = [];
  emitSubtitle("");
  if (!props.slide.subtitles) return;
  try {
    const response = await fetch(resolvePublicAsset(props.slide.subtitles));
    subtitleEvents.value = response.ok ? await response.json() : [];
  } catch { subtitleEvents.value = []; }
}
function resolvePublicAsset(path) {
  if (!path) return "";
  if (/^(https?:)?\/\//.test(path) || path.startsWith("data:")) return path;
  const base = import.meta.env.BASE_URL || "/";
  const normalizedBase = base.endsWith("/") ? base : `${base}/`;
  return `${normalizedBase}${String(path).replace(/^\/+/, "")}`;
}
function syncDuration() { duration.value = Number.isFinite(audio.value?.duration) ? audio.value.duration : 0; }
function syncSubtitle() {
  const time = audio.value?.currentTime ?? 0;
  const activeIndex = subtitleEvents.value.findIndex((item) => time >= item.start && time < item.end);
  emitSubtitle(subtitleEvents.value[activeIndex]?.text ?? "");
  emit("subtitle-index-change", activeIndex);
}
function syncPlayback() {
  if (!seeking.value) currentTime.value = audio.value?.currentTime ?? 0;
  emit("time-update", currentTime.value);
  syncDuration();
  syncSubtitle();
}
function beginSeek() { resumeAfterSeek.value = !audio.value?.paused; seeking.value = true; }
function endSeek() { seeking.value = false; syncPlayback(); if (resumeAfterSeek.value) playCurrent(); }
function handleEnded() {
  emitSubtitle("");
  currentTime.value = duration.value;
  emit("time-update", currentTime.value);
  if (!isLastSlide.value && nextRoute.value) router.push(nextRoute.value);
  else { audio.value?.pause(); playing.value = false; }
}
function formatTime(seconds) {
  const safe = Number.isFinite(seconds) ? Math.max(0, Math.floor(seconds)) : 0;
  return `${Math.floor(safe / 60)}:${(safe % 60).toString().padStart(2, "0")}`;
}
watch(() => props.slide.slideId, async () => {
  initialPlayRequested.value = false;
  currentTime.value = 0;
  duration.value = 0;
  emit("time-update", 0);
  await loadSubtitles();
  await nextTick();
  audio.value?.load();
  window.setTimeout(requestInitialPlayback, 100);
});
onMounted(async () => {
  await loadSubtitles();
  window.setTimeout(requestInitialPlayback, 100);
});
onBeforeUnmount(() => { audio.value?.pause(); });
defineExpose({ toggle, goNext, goPrev, playCurrent });
</script>
