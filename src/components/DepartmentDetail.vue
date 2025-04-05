<template>
  <div class="container">
    <div class="indicator">{{ deptEngName }}</div>
    <div class="content" :style="`left: ${offsetX}%; top: ${offsetY}%;`">
      <div class="title animate delay1">{{ deptName }}</div>
      <div class="line animate delay2"></div>
      <div class="main animate">{{ deptIntroduction }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
const {
  deptName, deptEngName, deptIntroduction, offsetX = 50, offsetY = 50
} = defineProps<{
  deptName: string
  deptEngName: string
  deptIntroduction: string
  offsetX?: number
  offsetY?: number
}>();

</script>

<style scoped>
div.container {
  pointer-events: none;
  position: absolute;
  height: 100%;
  width: 100%;
  background-color: transparent;
  transition: opacity 1.0s ease 0.5s;
}

div.indicator {
  position: absolute;
  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
  bottom: 20%;
  left: 60%;
  color: var(--kx-dark-neglect);
  mask-image: linear-gradient(transparent 30%, rgba(0,0,0,0.3) 70%);
  font-size: 10vmax;
  width: max-content;
  transition: opacity 500ms ease-in-out;
}

div.content {
  position: absolute;
  display: flex;
  flex-direction: column;
  justify-content: center;
  translate: -50% -50%;
  height: 40%;
  width: 30%;
  overflow: hidden;
  font-family: Arial, Helvetica, sans-serif;
}

div.content .main {
  font-size: 1vmax;
  color: var(--kx-dark-white0);
  transition: translate 500ms ease;
  transition-delay: 100ms;
}

div.content .title {
  font-weight: bold;
  font-size: 3vmax;
  color: var(--kx-dark-white0);
  transition: translate 500ms ease;
  transition-delay: 200ms;
}

div.content .line {
  height: 5px;
  width: 100%;
  background-color: var(--kx-dark-activate);
  margin-top: 10px;
  margin-bottom: 10px;
  transition: translate 500ms ease;
}

</style>