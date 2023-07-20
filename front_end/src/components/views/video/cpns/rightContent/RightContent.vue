<template>
  <div class="container">
    <div class="container-header">
      <span class="title">文本</span>
      <span class="export">导出</span>
    </div>
    <div class="content" v-if="videoInfo?.lyric.length">
      <template v-for="(item, index) of videoInfo.lyric">
        <el-tooltip
          :content="getTooltip(item.bg, item.ed)"
          :hide-after="50"
          placement="left"
          effect="customized"
        >
          <div
            contenteditable="true"
            class="sentence"
            :class="{
              'sentence-select': isHighlighted(index + 1),
            }"
            @click="handleContentClick(index + 1)"
          >
            {{ item.line }}
          </div>
        </el-tooltip>
      </template>
    </div>
    <el-skeleton :rows="16" animated v-else />
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { useRoute } from "vue-router";
import useVideoList from "~/stores/videoList/videoList";
import { ref } from "vue";
import { durationFormat } from "~/utils/datatime";

// 异步数据不适合传给props 直接从videoList中调用
const orderId = useRoute().fullPath.slice(7); //根据路由获取orderId
console.log(orderId);
const videoListStore = useVideoList();
const { videos } = storeToRefs(videoListStore);
const videoIndex = videoListStore.findVideoIndex(orderId);
const videoInfo = videos.value[videoIndex];
// TODO: 返回 选定的区间 用 emit + 一个小按钮

// 处理点击 选中文本逻辑
const startIndex = ref(-1);
const endIndex = ref(-1);
const handleContentClick = function (index: number) {
  console.log("index", index);
  console.log("startIndex.value: ", startIndex.value);
  console.log("endIndex.value: ", endIndex.value);
  if (startIndex.value === -1) {
    //00
    startIndex.value = index;
  } else if (endIndex.value !== -1 && startIndex.value !== -1) {
    // 11
    startIndex.value = index;
    endIndex.value = -1;
    videoListStore.updateLyricIndex(
      startIndex.value,
      endIndex.value,
      videoIndex
    );
  } else if (startIndex.value !== -1) {
    //10
    if (index < startIndex.value) {
      // 选中的end 小于start
      startIndex.value = -1;
      endIndex.value = -1;
      videoListStore.updateLyricIndex(
        startIndex.value,
        endIndex.value,
        videoIndex
      );
    } else {
      endIndex.value = index;
      videoListStore.updateLyricIndex(
        startIndex.value,
        endIndex.value,
        videoIndex
      );
    }
  }
  console.log("startIndex.value: ", startIndex.value);
  console.log("endIndex.value: ", endIndex.value);
};
// 处理 高亮逻辑
const isHighlighted = (index: number) => {
  return (
    (index >= startIndex.value && index <= endIndex.value) ||
    index === startIndex.value ||
    index === endIndex.value
  );
};

const getTooltip = (bg: string, ed: string) => {
  return durationFormat(bg) + "--" + durationFormat(ed);
};
</script>

<style scoped lang="scss">
.container {
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  box-sizing: border-box;
  padding: 30px 70px 50px 70px;
  .container-header {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 0 0 16px 0;
    .title {
      color: #0000008c;
      font-size: medium;
    }
    .export {
      padding: 5px 13px;
      color: #738298;
      font-size: 14px;
      text-align: center;
      border: 1px solid #bcc4cf;
      border-radius: 100px;
      &:hover {
        cursor: pointer;
      }
    }
  }
  .content {
    .sentence {
      display: inline;
      line-height: 1.7;
      outline: none;
      -webkit-transition: 0.3s all ease;
      transition: 0.3s all ease;
      -webkit-user-select: none;
      -moz-user-select: none;
      -ms-user-select: none;
      user-select: none;
      word-break: break-all;
      font-size: 20px;
      padding: 0;
      margin: 0;
      &:hover {
        font-weight: bold;
      }
    }
    .sentence-select {
      font-weight: bold;
    }
  }
}
</style>
