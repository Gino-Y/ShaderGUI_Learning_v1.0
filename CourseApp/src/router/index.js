import { createRouter, createWebHistory } from "vue-router";
import CourseHome from "../views/CourseHome.vue";
import QuizView from "../views/QuizView.vue";
import SlideView from "../views/SlideView.vue";
import ExploreView from "../views/ExploreView.vue";

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: CourseHome },
    { path: "/module/:moduleId", redirect: "/" },
    { path: "/module/:moduleId/slide/:slideId", component: SlideView },
    { path: "/module/:moduleId/slide/:slideId/explore", component: ExploreView },
    { path: "/module/:moduleId/quiz", component: QuizView },
    { path: "/:pathMatch(.*)*", redirect: "/" },
  ],
});
