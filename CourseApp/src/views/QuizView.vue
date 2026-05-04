<template>
  <main class="min-h-screen bg-neutral-950 px-4 py-6 text-white sm:px-8">
    <section v-if="quiz && !finished" class="mx-auto grid max-w-3xl gap-5">
      <BreadcrumbNav :module-id="moduleId" label="做题页" class="text-white" />
      <header class="rounded-lg border border-white/10 bg-white/[0.04] p-5">
        <p class="text-sm font-semibold text-emerald-300">{{ currentIndex + 1 }} / {{ attempt.length }}</p>
        <h1 class="mt-2 text-2xl font-semibold">{{ currentQuestion.prompt }}</h1>
      </header>
      <article class="rounded-lg border border-white/10 bg-white/[0.04] p-5">
        <div class="grid gap-3">
          <label
            v-for="option in currentQuestion.options"
            :key="option.id"
            class="flex cursor-pointer items-center gap-3 rounded-md border border-white/10 bg-neutral-900 px-4 py-3"
          >
            <input v-if="currentQuestion.type === 'multiple'" v-model="answers[currentQuestion.id]" :value="option.id" type="checkbox" class="accent-emerald-400" />
            <input v-else v-model="answers[currentQuestion.id]" :value="option.id" type="radio" class="accent-emerald-400" />
            <span class="text-sm font-semibold text-emerald-200">{{ option.label }}</span>
            <span>{{ option.text }}</span>
          </label>
        </div>
        <div class="mt-5 flex flex-wrap gap-3">
          <button class="rounded-md bg-emerald-500 px-4 py-2 font-semibold text-neutral-950" type="button" @click="submitQuiz">提交答案</button>
          <button class="rounded-md border border-white/15 px-4 py-2" type="button" @click="resetCurrent">重置</button>
        </div>
      </article>
    </section>
    <section v-else-if="quiz" class="mx-auto grid max-w-4xl gap-5">
      <BreadcrumbNav :module-id="moduleId" label="成绩" class="text-white" />
      <article class="rounded-lg border border-white/10 bg-white/[0.04] p-6 text-center">
        <p class="text-sm font-semibold text-emerald-300">完成</p>
        <h1 class="mt-2 text-4xl font-semibold">本次得分 {{ score }} / {{ attempt.length }}</h1>
        <div class="mt-6 grid gap-4 text-left">
          <article v-for="item in review" :key="item.question.id" class="rounded-md border p-4" :class="item.correct ? 'border-emerald-400/50 bg-emerald-400/10' : 'border-rose-400/50 bg-rose-400/10'">
            <h2 class="text-lg font-semibold" :class="item.correct ? 'text-emerald-200' : 'text-rose-200'">{{ item.correct ? "正确" : "需复习" }} · {{ item.question.prompt }}</h2>
            <div class="mt-3 grid gap-2">
              <div v-for="option in item.question.options" :key="option.id" class="rounded-md border px-3 py-2" :class="optionClass(item, option.id)">
                <span class="mr-2 text-sm font-semibold">{{ option.label }}</span>{{ option.text }}
                <span v-if="item.answer.includes(option.id)" class="ml-2 rounded bg-white/10 px-2 py-0.5 text-xs">你的选择</span>
                <span v-if="item.question.answer.includes(option.id)" class="ml-2 rounded bg-emerald-400/20 px-2 py-0.5 text-xs text-emerald-100">正确答案</span>
              </div>
            </div>
            <p v-if="!item.correct" class="mt-3 rounded-md bg-black/20 px-3 py-2 text-white/85">
              {{ missSummary(item) }}
            </p>
            <p class="mt-3 text-white/75">{{ item.question.explanation }}</p>
          </article>
        </div>
        <div class="mt-6 flex flex-wrap justify-center gap-3">
          <button class="rounded-md bg-emerald-500 px-4 py-2 font-semibold text-neutral-950" type="button" @click="restartQuiz">重新挑战</button>
          <button class="rounded-md border border-emerald-400/60 px-4 py-2 text-emerald-100" type="button" @click="continuePractice">继续练习</button>
          <RouterLink :to="currentCourseRoute" class="rounded-md border border-white/15 px-4 py-2">回到当前课程</RouterLink>
          <RouterLink v-if="nextLessonRoute" :to="nextLessonRoute" class="rounded-md border border-white/15 px-4 py-2">下一课</RouterLink>
          <span v-else class="rounded-md border border-white/10 px-4 py-2 text-white/35">下一课不可用</span>
          <RouterLink to="/" class="rounded-md border border-white/15 px-4 py-2">回到菜单</RouterLink>
        </div>
      </article>
    </section>
  </main>
</template>
<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import BreadcrumbNav from "../components/BreadcrumbNav.vue";
import quizzes from "../data/quizzes.json";
import slides from "../data/slides.json";

const route = useRoute();
const moduleId = computed(() => String(route.params.moduleId));
const quiz = computed(() => quizzes.find((item) => item.moduleId === moduleId.value));
const attempt = ref([]);
const currentIndex = ref(0);
const answers = ref({});
const finished = ref(false);
const currentQuestion = computed(() => attempt.value[currentIndex.value] || {});
const score = computed(() => review.value.filter((item) => item.correct).length);
const moduleSlides = computed(() =>
  slides.filter((item) => item.moduleId === moduleId.value).sort((a, b) => a.order - b.order),
);
const currentCourseRoute = computed(() => moduleSlides.value[0]?.route || "/");
const nextLessonRoute = computed(() => moduleSlides.value[1]?.route || "");
const review = computed(() => attempt.value.map((question) => {
  const answer = normalize(answers.value[question.id]);
  const correctAnswer = normalize(question.answer);
  return {
    question,
    answer,
    correct: answer.length === correctAnswer.length && correctAnswer.every((id) => answer.includes(id)),
  };
}));
function shuffle(items) {
  const copy = [...items];
  for (let index = copy.length - 1; index > 0; index -= 1) {
    const swapIndex = Math.floor(Math.random() * (index + 1));
    [copy[index], copy[swapIndex]] = [copy[swapIndex], copy[index]];
  }
  return copy;
}
function labelOptions(question) {
  return { ...question, options: shuffle(question.options).map((option, index) => ({ ...option, label: "ABCD"[index] })) };
}
function restartQuiz() {
  attempt.value = shuffle(quiz.value.questions).slice(0, 3).map(labelOptions);
  answers.value = Object.fromEntries(attempt.value.map((question) => [question.id, question.type === "multiple" ? [] : ""]));
  currentIndex.value = 0;
  finished.value = false;
}
function continuePractice() {
  restartQuiz();
}
function normalize(value) {
  if (Array.isArray(value)) return [...value].sort();
  return value ? [value] : [];
}
function submitQuiz() {
  if (currentIndex.value < attempt.value.length - 1) currentIndex.value += 1;
  else finished.value = true;
}
function resetCurrent() {
  answers.value[currentQuestion.value.id] = currentQuestion.value.type === "multiple" ? [] : "";
}
function optionClass(item, id) {
  if (item.question.answer.includes(id) && item.answer.includes(id)) return "border-emerald-400/60 bg-emerald-400/15";
  if (item.question.answer.includes(id)) return "border-yellow-400/60 bg-yellow-400/10";
  if (item.answer.includes(id)) return "border-rose-400/60 bg-rose-400/15";
  return "border-white/10 bg-neutral-900";
}
function missSummary(item) {
  const missed = item.question.answer.filter((id) => !item.answer.includes(id)).length;
  const wrong = item.answer.filter((id) => !item.question.answer.includes(id)).length;
  return `漏选 ${missed} 项，误选 ${wrong} 项；请对照上方标签复盘。`;
}
onMounted(() => {
  if (quiz.value) restartQuiz();
});
</script>
