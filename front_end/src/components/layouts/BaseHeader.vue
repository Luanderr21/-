<script lang="ts" setup>
import { toggleDark } from "~/composables";
import Icon from "../icon.vue";
import useVideoList from "~/stores/videoList";
import { storeToRefs } from "pinia";
import { reactive } from "vue";
const videoListStore = useVideoList();

const { videos } = reactive(videoListStore);
console.log("videos: ", videos);
</script>

<template>
  <el-header>
    <el-menu mode="horizontal" :ellipsis="false">
      <el-menu-item index="0" class="icon-col"><Icon /></el-menu-item>
      <div class="flex-grow" />
      <el-sub-menu index="2">
        <template #title>已上传视频</template>
        <template v-for="(item, index) in videos">
          <el-menu-item :index="item.index">{{ item.name }}</el-menu-item>
        </template>
      </el-sub-menu>
    </el-menu>
  </el-header>
</template>

<style scoped>
.icon-col {
  width: 100px;
}
</style>
