<template>
  <el-config-provider namespace="ep">
    <BaseHeader />
    <div class="main">
      <router-view v-slot="{ Component }" :key="route.path">
        <keep-alive>
          <transition>
            <component :is="Component" />
          </transition>
        </keep-alive>
      </router-view>
    </div>
  </el-config-provider>
</template>

<style>
body {
  height: 100vh;
  width: 100wh;
}
#app {
  color: var(--ep-text-color-primary);
  height: 100%;
}
.main {
  /* flex: 1; */
  height: calc(100vh - 60px);
}
</style>

<script setup lang="ts">
import { watch, ref } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
// const route = useRoute();
// console.log(route);
// let Component: Vnode = ref();

// watch();
</script>
