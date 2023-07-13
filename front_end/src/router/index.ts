import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    alias: ["/home", "/home2"], // 别名，可以定义很多个
    component: () => import("~/components/views/home/home.vue"),
  },
  {
    path: "/video/:id",
    name: "video",
    component: () => import("~/components/views/video/video.vue"),
    // // 重定向
    // // redirect: '/welcome',
    // redirect: to => {
    //   console.log(to);
    //   return {
    //     path: '/welcome',
    //     query: {
    //       name: '欢迎'
    //     }
    //   }
    // },
    // children: [
    //   {
    //     path: '/welcome',
    //     name: 'welcome',
    //     component: () => import('../views/welcome.vue')    // component: import('../views/reg.vue')
    //   }
    // ]
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
