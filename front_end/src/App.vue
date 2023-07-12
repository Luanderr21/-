<template>
  <el-config-provider namespace="ep">
    <BaseHeader />
    <div class="main">
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </div>
  </el-config-provider>
</template>

<style scoped>
#app {
  color: var(--ep-text-color-primary);
}
.main {
  height: 650px;
}
</style>

<script setup lang="ts">
import { watch, ref } from "vue";
import { useRoute } from "vue-router";

// const route = useRoute();
// console.log(route);
// let Component: Vnode = ref();

// watch();
</script>
