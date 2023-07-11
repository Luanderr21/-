<template>
  <el-config-provider namespace="ep">
    <BaseHeader />
    <el-main>
      <router-view></router-view>
    </el-main>
  </el-config-provider>
</template>

<style>
#app {
  color: var(--ep-text-color-primary);
}
</style>

<script setup lang="ts"></script>
