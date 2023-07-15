<template>
  <SplitPane :max-width="700" :min-width="300" class="split-pan">
    <template #left-content
      ><MyVideo :src="getVideoSrc"></MyVideo>
      <AudioRecord></AudioRecord>
    </template>
    <template #right-content>
      <RightContent></RightContent>
    </template>
  </SplitPane>
</template>

<script setup lang="ts">
import { onMounted, watch, computed, ref } from "vue";
import { useRoute } from "vue-router";
import { queryText } from "~/service/api/query";
import { storeToRefs } from "pinia";
import useVideoList from "~/stores/videoList/videoList";
import { LyricItem } from "~/stores/videoList/types";
// KNOW: 第一次遇到206
import AudioRecord from "~/components/views/video/cpns/aduioRecord/AduioRecord.vue";

const orderId = ref(useRoute().fullPath.slice(7)); //根据路由获取orderId.value
console.log(orderId.value);
// TODO: 处理每次进入没有 orderID 的问题

// TODO: 处理轮询
const startPolling = async function () {
  let res = await fetchData();
  const poll = async () => {
    setTimeout(async () => {
      res = await fetchData();
      console.log(res);
      if (typeof res === "object") {
        storeLyric(res);
        return res;
      }
      poll();
    }, 5000);
  };
  poll();
};
const fetchData = async function () {
  const { data } = await queryText(orderId.value);
  console.log("fetchData", data);
  if (data === "failed!") {
    // TODO: 处理错误
    console.log("上传发生错误");
    return "上传错误";
  } else if (typeof data === "object") {
    return data;
  }
  return true;
};

const videoListStore = useVideoList();
const { videos } = storeToRefs(videoListStore);
const videoIndex = videoListStore.findVideoIndex(orderId.value);
const videoInfo = videos.value[videoIndex];
const storeLyric = function (lyric: LyricItem[]) {
  videoListStore.updateLyric(orderId.value, lyric);
};

const getVideoSrc = computed(() => {
  return videoInfo?.fileName === ""
    ? `http://127.0.0.1:5000/video_show?vkey=${orderId.value}`
    : `http://127.0.0.1:5000/video_show?vname=${videoInfo?.fileName}`;
});

onMounted(() => {
  startPolling();
  watch(useRoute().params, (toParams, previousParams) => {
    console.log("toParams, previousParams: ", toParams, previousParams);
    // 对路由变化做出响应...
  });
});
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
