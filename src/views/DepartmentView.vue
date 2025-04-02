<template>
  <FrameWrapper>
    <div class="button-left" @click="() => {buttonClick(-1)}">
      
    </div>
    <div class="button-right" @click="() => {buttonClick(1)}">

    </div>
    <canvas class="vfx" ref="vfx" :width="width" :height="height"></canvas>
    <div class="background"></div>
    <p class="back-text">Departments</p>
  </FrameWrapper>
</template>

<script setup lang="ts">
import FrameWrapper from '@/components/FrameWrapper.vue';
import { onMounted, onUnmounted, useTemplateRef } from 'vue';
import {
  startAnimation, stopAnimation, updateWindowSize, adjustIndex
} from '@/package/points';
import { ref } from 'vue';

const canvas = useTemplateRef("vfx")
const height = ref(0)
const width = ref(0)
let resizing: boolean = false

function buttonClick(direction: number) {
  adjustIndex(direction)
}

function resizeHandler() {
  if (!resizing) {
    resizing = true
    setTimeout(() => {
      resizing = false
      height.value = window.innerHeight
      width.value = window.innerWidth
      updateWindowSize()
    }, 250);
  }
}

onMounted(() => {
  height.value = window.innerHeight
  width.value = window.innerWidth
  window.addEventListener("resize", resizeHandler)
  startAnimation(canvas.value as HTMLCanvasElement)
})

onUnmounted(() => {
  window.removeEventListener('resize', resizeHandler)
  stopAnimation()
})

</script>

<style scoped>
.button-left {
  position: absolute;
  background-color: red;
  top: 50%;
  left: 10%;
  width: 100px;
  height: 200px;
  translate: -50% -50%;
}

.button-right {
  position: absolute;
  background-color: red;
  top: 50%;
  right: 10%;
  width: 100px;
  height: 200px;
  translate: 50% -50%;
}

canvas.vfx {
  position: absolute;
  pointer-events: none;
  z-index: -1;
  scale: 0.8 0.8;
}

div.background {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image:
    linear-gradient(rgba(255,255,255,.5) 2px, transparent 2px),
    linear-gradient(90deg, rgba(255,255,255,.5) 2px, transparent 2px),
    linear-gradient(rgba(255,255,255,.3) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,.3) 1px, transparent 1px);
  background-size: 100px 100px, 100px 100px, 20px 20px, 20px 20px;
  background-position:-2px -2px, -2px -2px, -1px -1px, -1px -1px;
  mask-image: radial-gradient(rgba(0, 0, 0, 0.2), transparent 80%);
  mask-mode: alpha;

  transition:
    scale 1.5s ease,
    opacity 1.5s ease;
  
  z-index: -3;
}

.forward-enter-from div.background {
  opacity: 0;
  scale: 0.5 0.5;
}
.rewind-enter-from div.background {
  opacity: 0;
  scale: 0.5 0.5;
}

p.back-text {
  position: absolute;
  pointer-events: none;
  top: 85%;
  left: 5%;
  display: block;
  font-size: 4vw;
  font-family: 'Times New Roman', Times, serif;
  font-weight: bold;
  color: var(--kx-dark-neglect);
  z-index: -2;
}

</style>