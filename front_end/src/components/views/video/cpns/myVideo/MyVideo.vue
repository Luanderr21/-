<script setup lang="ts">
import { storeToRefs } from "pinia";
import { onMounted, ref, nextTick, computed, watch } from "vue";
import { useRoute } from "vue-router";

import useVideoListStore from "~/stores/videoList/videoList";

// import videojs from "video.js";
// import videojs, { VideoJsPlayerOptions, VideoJsPlayer } from "video.js";
// import "video.js/dist/video-js.min.css";

type MyVideoProps = {
  /** 视频地址 */
  src: string;
  width?: string;
  height?: string;
};
const props = withDefaults(defineProps<MyVideoProps>(), {});
// video标签
const videoRef = ref<HTMLVideoElement | null>(null);
// video实例对象
// let videoPlayer: VideoJsPlayer | null = null;

// const videoWrapStyles = computed<CSSProperties>(() => {
//   return {
//     width: props.width || "100%",
//     height: props.height || "80%",
//   };
// });
// 初始化videojs
// const initVideo = async () => {
//   // https://gitcode.gitcode.host/docs-cn/video.js-docs-cn/docs/guides/options.html
//   await nextTick();
//   const options: VideoJsPlayerOptions = {
//     language: "zh-CN", // 设置语言
//     controls: true, // 是否显示控制条
//     preload: "auto", // 预加载
//     autoplay: false, // 是否自动播放
//     fluid: false, // 自适应宽高
//     src: {
//       src: props.src,
//       type: "video/mp4",
//     }, // 要嵌入的视频源的源 URL
//   };
//   if (videoRef.value) {
//     // 创建 video 实例
//     videoPlayer = videojs(videoRef.value, options, onPlayerReady);
//   }
// };
// video初始化完成的回调函数
// const onPlayerReady = () => {};
// onMounted(() => {
//   // initVideo();
// });

// 处理字幕逻辑
let currentTime = ref(0);
// 处理时间
const handleTimeUpdate = () => {
  // 更新当前时间
  currentTime.value = videoRef.value?.currentTime ?? 0;
};

// 处理加载逻辑
const videoListStore = useVideoListStore();
const { videos } = storeToRefs(videoListStore);
const orderId = useRoute().fullPath.slice(7);
const videoIndex = videoListStore.findVideoIndex(orderId);

const isVideoLoading = computed(() => {
  return videos.value[videoIndex].status == "waiting";
});
</script>
<template>
  <div class="video-container" v-loading="isVideoLoading">
    <video
      id="my-player"
      ref="videoRef"
      class="video-js w-full h-full"
      @timeupdate="handleTimeUpdate"
      :src="src"
      controls
    ></video>
  </div>
  <subTitle :current-time="currentTime"></subTitle>
</template>
<style lang="scss" scoped>
.video-container {
  position: relative;
  width: 100%;
  height: 0;
  padding-bottom: calc(9 / 16 * 100%); // 根据视频比例设置高度
}
.video-js {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
