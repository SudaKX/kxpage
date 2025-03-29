<script setup lang="ts">
import FrameWrapper from '@/components/FrameWrapper.vue';
</script>

<template>
  <FrameWrapper>
    <div class="layout">
      <h1>Home view</h1>
    </div>
  </FrameWrapper>
</template>

<style lang="css" scoped>
.layout {
  position: absolute;
  height: 100%;
  width: 100%;
  background: purple;
}
.layout h1 {
  position: relative;
  display: block;
  top: 50%;
}
</style>
