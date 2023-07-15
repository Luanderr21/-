import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
// import { storeToRefs } from "pinia";
// import { useRoute, useRouter } from "vue-router";
// import useVideoList from "~/stores/videoList/videoList";
// const videoListStore = useVideoList();
// const { videos } = storeToRefs(videoListStore);
// const routerObj = useRouter();
// 最后决定在组件里面写

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
    // beforeEnter: (to, from) =>{
    //   const videoIndex = videos.value.findIndex(
    //     (item) => "/video/" + item.orderId === useRoute().fullPath
    //   );
    //   if(!videoIndex){
    //     return false
    //   }
    // }
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
