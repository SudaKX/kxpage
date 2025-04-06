<template>
  <div class="button to-left" @click="() => {changeDept(-1)}">
    <svg viewBox="0 0 100 50">
      <polygon points="0,0 20,0 50,30 60,40 50,50" />
      <polygon points="80,0 100,0 70,30 60,20"/>
    </svg>
  </div>
  <div class="button to-right" @click="() => {changeDept(1)}">
    <svg viewBox="0 0 100 50">
      <polygon points="0,0 20,0 50,30 60,40 50,50" />
      <polygon points="80,0 100,0 70,30 60,20"/>
    </svg>
  </div>
  <Transition name="dpc" :duration="700" mode="out-in">
    <component :is="DepartmentDetail" v-bind="deptDetail" :key="currentDepartment">
    </component>
  </Transition>
  <div class="length">
    <div class="highlight" :style="pageIndicatorStyle"></div>
  </div>
</template>

<script setup lang="ts">
import DepartmentDetail from './DepartmentDetail.vue';
import { computed, ref } from 'vue';
import { adjustIndex } from '@/package/points';
import { departmentDescription } from '@/package/staticData';

const detailSpecs = departmentDescription;
const currentDepartment = ref(0)
const detailSpecSize: number = detailSpecs.length
const deptDetail = computed(() => detailSpecs[currentDepartment.value])
const pageIndicatorStyle = computed(() => {
  let width = 100 / (detailSpecSize - 1);
  let left = (currentDepartment.value - 1) * width;
  if (currentDepartment.value == 0) {
    left = 0;
    width = 100;
  }
  return `left: ${left}%; width: ${width}%;`;
})

function changeDept(step: number) {
  const temp = currentDepartment.value + step
  adjustIndex(step)
  if (temp < 0) {
    currentDepartment.value = temp + detailSpecSize
  } else if (temp >= detailSpecSize) {
    currentDepartment.value = temp - detailSpecSize
  } else {
    currentDepartment.value = temp
  }
}

</script>

<style scoped>

div.button {
  display: flex;
  position: absolute;
  width: 5vw;
  height: 15vh;
  align-items: center;
  transition:
    opacity 1.0s ease 0.5s,
    scale 200ms ease-in-out;
  z-index: 1;
}

div.button:hover {
  scale: 1.1;
}

div.button:active {
  scale: 1.0;
}

div.button svg {
  fill: var(--kx-dark-neglect-light);
  transition: fill 200ms ease-in-out;
  scale: 1.5 1.2;
}

div.button:hover svg{
  fill: var(--kx-dark-activate);
}

div.button:active svg {
  fill: var(--kx-dark-activate-dark);
}

div.to-left svg {
  rotate: 90deg;
}

div.to-right svg {
  rotate: -90deg;
}

div.to-left {
  top: 50%;
  left: 8%;
  translate: -50% -50%;
}

div.to-right {
  top: 50%;
  right: 8%;
  translate: 50% -50%;
}

.dpc-enter-from :deep(.indicator) {
  opacity: 0;
}

.dpc-enter-from :deep(.animate) {
  translate: -100% 0
}

.dpc-leave-active :deep(div.delay1) {
  transition-delay: 100ms;
}
.dpc-leave-active :deep(div.delay2) {
  transition-delay: 200ms;
}

.dpc-leave-to :deep(.animate) {
  translate: 100% 0
}

.dpc-leave-to :deep(.indicator) {
  opacity: 0;
}

div.length {
  position: absolute;
  pointer-events: none;
  top: 85%;
  left: 5%;
  width: 15vmax;
  height: 2.4vmax;
  display: block;
  background-color: var(--kx-dark-neglect);
  mask-image: url("/deptMask.svg");
  mask-size: contain;
  mask-repeat: no-repeat;
  mask-position: 0 0;
  z-index: -2;
}

div.length>div.highlight {
  position: absolute;
  height: 100%;
  background-color: var(--kx-dark-activate);
  transition:
    left 200ms ease-in-out,
    width 200ms ease;
}

</style>