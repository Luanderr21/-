<template>
  <div class="subtitle">
    {{ currentSubtitle }}
  </div>
</template>

<script setup lang="ts">
import { toRefs, reactive, computed, toRef, ref, watch, onMounted } from "vue";
import useVideoList from "~/stores/videoList/videoList";
import { storeToRefs } from "pinia";
import { useRoute } from "vue-router";
import { onActivated } from "vue";

const props = defineProps<{
  currentTime: number;
}>();
console.log(props.currentTime);
const currentTime = toRef(props, "currentTime");
// 处理字幕逻辑
const orderId = ref(useRoute().fullPath.slice(7)); //根据路由获取orderId
const videoListStore = useVideoList();
const { videos } = storeToRefs(videoListStore);
const videoIndex = ref(videoListStore.findVideoIndex(orderId.value));
let lyric = videos.value[videoIndex.value].lyric;

const getCurrentLyricIndex = () => {
  let thisCurrentTime = currentTime.value * 1000;
  let left = 0;
  let right = lyric.length - 1;

  // 利用二分查找 找到对应的 index
  while (left <= right) {
    const mid = Math.floor((left + right) / 2);
    const { bg, ed } = lyric[mid];

    const bgTime = parseInt(bg); // 将时间字符串解析为毫秒数
    const edTime = parseInt(ed);
    // console.log(bgTime, edTime, thisCurrentTime);

    if (thisCurrentTime >= bgTime && thisCurrentTime < edTime) {
      // console.log(mid);
      return mid; // 当前时间在该字幕范围内，返回索引
    } else if (thisCurrentTime < bgTime) {
      right = mid - 1; // 当前时间在字幕范围的左侧，向左查找
    } else {
      left = mid + 1; // 当前时间在字幕范围的右侧，向右查找
    }
  }

  return -1; // 找不到对应的字幕，返回 -1
};

const currentSubtitle = ref("等待视频播放");

// 解决数据异步更新，但是lyric不更新的问题
watch(
  videos,
  (old, newValue) => {
    if (newValue[videoIndex.value].status === "waiting") {
      currentSubtitle.value = "等待视频转换";
    }
    lyric = videos.value[videoIndex.value].lyric;
  },
  {
    deep: true,
  }
);
// 监听 lyric 和 currentTime 的变化，重新计算 currentSubtitle
watch([lyric, currentTime], () => {
  currentSubtitle.value = lyric[getCurrentLyricIndex()]?.line ?? "";
});
watch(
  () => useRoute().fullPath.slice(7),
  (o, n) => {
    console.log(o, n);
  }
);
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
