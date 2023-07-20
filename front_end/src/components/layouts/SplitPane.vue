<script setup lang="ts">
import { onMounted, ref } from "vue";
import useVideoList from "~/stores/videoList/videoList";
import { storeToRefs } from "pinia";
import { useRoute } from "vue-router";

const orderId = useRoute().fullPath.slice(7); //根据路由获取orderId
const videoListStore = useVideoList();
const { videos } = storeToRefs(videoListStore);
const videoIndex = videoListStore.findVideoIndex(orderId);

// watch(videos.value[videoIndex].lyric, (newValue, oldValue) => {
//   console.log(newValue, oldValue);
//   if (newValue.length === 0) {
//     isLoading.value = true;
//   } else {
//     isLoading.value = false;
//   }
// });

onMounted(() => {
  dragControllerDiv();
});

function dragControllerDiv() {
  let resize = document.getElementsByClassName(
    "resize"
  ) as HTMLCollectionOf<HTMLElement>;
  let boxDom = document.getElementsByClassName(
    "box"
  ) as HTMLCollectionOf<HTMLElement>;
  let leftDom = document.getElementsByClassName(
    "left"
  ) as HTMLCollectionOf<HTMLElement>;
  let rightDom = document.getElementsByClassName(
    "right"
  ) as HTMLCollectionOf<HTMLElement>;

  for (let i = 0; i < resize.length; i++) {
    /*鼠标 按下拖拽区 */
    resize[i].onmousedown = function (e) {
      // 拖拽区 变色
      resize[i].style.background = "#818181";
      // 拖拽区 开始的距离  403
      var startX = e.clientX;

      // 左边大小 放入 resize
      (resize[i] as any).left = resize[i].offsetLeft;

      /* 鼠标拖拽 */
      document.onmousemove = function (ee) {
        // 拖拽区 结束的距离
        var endX = ee.clientX;

        // 移动的距离 （endx-startx）=移动的距离。resize[i].left+移动的距离=左边区域最后的宽度
        let leftWidth = (resize[i] as any).left + (endX - startX);

        // 右边最大宽度
        let maxWidth = boxDom[i].clientWidth - resize[i].offsetWidth;

        /* 设置 左边 最小值 */
        if (leftWidth < 400) leftWidth = 400;
        if (leftWidth > maxWidth - 400) leftWidth = maxWidth - 400;

        // 设置拖拽条 距离左侧区域的宽度
        resize[i].style.left = leftWidth;
        // 设置 左边宽度
        leftDom[i].style.width = leftWidth + "px";
        // 设置右边宽度
        rightDom[i].style.width =
          boxDom[i].clientWidth - leftWidth - resize[i].offsetWidth + "px";
      };

      /* 鼠标松开 */
      document.onmouseup = function () {
        // 取消事件
        document.onmousemove = null;
        document.onmouseup = null;
        // 恢复颜色
        resize[i].style.background = "#d6d6d6";
      };
    };
  }

  return false;
}
</script>

<template>
  <div class="box">
    <div class="left" id="left">
      <slot name="left-content"></slot>
    </div>
    <div
      class="resize"
      title="收缩侧边栏"
      style="background-color: white"
    ></div>
    <div class="right">
      <slot name="right-content"></slot>
    </div>
  </div>
</template>

<style lang="scss">
.box {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  padding: 10px 20px 10px 20px;
  display: flex;
  position: relative;
  .left {
    width: 60%;
    height: 100%;
    box-sizing: border-box;
    padding: 10px 20px 10px 20px;
    background-color: rgb(206, 214, 224);
    display: flex;
    flex-flow: column nowrap;
    overflow-y: scroll;
  }
  .left::-webkit-scrollbar {
    display: none;
  }
  .right {
    width: 40%;
    height: 100%;
    background-color: rgb(206, 214, 224);
    overflow-y: scroll;
  }
  /*拖拽区div样式*/
  .resize {
    cursor: col-resize;
    width: 3px;
    height: 100%;
    background-size: cover;
    background-position: center;
    background-color: #fff;
  }
  /*拖拽区鼠标悬停样式*/
  .resize:hover {
    color: #444444;
  }
}
</style>
