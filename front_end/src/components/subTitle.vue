<template>
  <div class="subtitle">
    {{ currentSubtitle }}
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import "video.js/dist/video-js.min.css";
import useVideoList from "~/stores/videoList/videoList";
import { storeToRefs } from "pinia";
import { useRoute } from "vue-router";

const props = withDefaults(
  defineProps<{
    currentTime: number;
  }>(),
  {
    currentTime: 0,
  }
);

const currentTime = ref(props.currentTime ?? 0);

// 处理字幕逻辑
const orderId = useRoute().fullPath.slice(7); //根据路由获取orderId
const currentSubtitle = ref("");
const videoListStore = useVideoList();
const { videos } = storeToRefs(videoListStore);
const videoIndex = videoListStore.findVideoIndex(orderId);
const lyric = reactive(videos.value[videoIndex].lyric);
currentSubtitle.value =
  lyric.find(
    (item) =>
      Number(item.bg) >= currentTime.value &&
      Number(item.ed) <= currentTime.value
  )?.line ?? "";
</script>

<style lang="scss" scoped>
.split-pan {
  height: 100%;
}

.subtitle {
  color: var(--ep-color-primary);
  box-sizing: border-box;
  width: 100%;
  padding: 30px 40px 30px 40px;
  text-align: center;
  line-height: 1.5;
  font-size: larger;
  border-radius: 30px;
  background-color: var(--ep-color-warning-light-9);
  margin-top: 20px;
}
</style>
