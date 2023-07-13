<template>
  <SplitPane :max-width="900" :min-width="300" class="split-pan">
    <template #left-content
      ><MyVideo
        src="https://cdn.jsdelivr.net/gh/xdlumia/files/video-play/IronMan.mp4"
      ></MyVideo
    ></template>
    <template #right-content>
      <div></div>
    </template>
  </SplitPane>
</template>

<script setup lang="ts"></script>

<style lang="scss">
.split-pan {
  height: 100%;
}
</style>
