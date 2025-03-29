<script setup lang="ts">
import FrameWrapper from '@/components/FrameWrapper.vue';
</script>

<template>
  <FrameWrapper>
    <div class="about">
      <h1>This is an about page</h1>
    </div>
  </FrameWrapper>
</template>

<style scoped>
.about {
  height: 100%;
  width: 100%;
  background-color: yellow;
}
h1 {
  position: absolute;
  display: block;
  top: 50%;
}
</style>
