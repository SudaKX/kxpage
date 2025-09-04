<template>
  <div class="contain">
    <div :class="scrollIndicatorState">
    <p class="tip-text">SCROLL</p>
    <svg class="arrow" viewBox="0 0 100 50">
      <polygon points="0,0 20,0 50,30 60,40 50,50" />
      <polygon points="80,0 100,0 70,30 60,20"/>
    </svg>
  </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useCurrentIndexStore } from '@/stores/currentIndex'
import { storeToRefs } from 'pinia'

const { currentIndex } = storeToRefs(useCurrentIndexStore())
const { maxIndex } = useCurrentIndexStore()
const scrollIndicatorState = ref("scroll-tip active")

watch(currentIndex, (value) => {
  if (value == 0) {
    scrollIndicatorState.value = "scroll-tip active"
  } else if (value == maxIndex) {
    scrollIndicatorState.value = "scroll-tip hide"
  } else {
    scrollIndicatorState.value = "scroll-tip inactive"
  }
})

</script>

<style scoped>
div.contain {
  position: absolute;
  pointer-events: none;
  width: 70px;
  height: 50px;
  top: 90vh;
  left: 50vw;
  transform: translateX(-50%);
}

.scroll-tip {
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: 2s tip-move infinite cubic-bezier(0.75, 0, 0.25, 1);
}

.tip-text {
  position: relative;
  color: var(--kx-dark-activate);
  display: block;
  font-family: sans-serif;
  font-size: 10px;
  transition: color 250ms linear;
}

.inactive .tip-text {
  color: gray;
}

.hide .tip-text {
  color: transparent;
}

svg.arrow {
  position: relative;
  fill: var(--kx-dark-activate);
  stroke-width: 0px;
  transition: fill 250ms linear;
  width: 50%;
}

.inactive svg.arrow {
  fill: gray;
}

.hide svg.arrow {
  fill: transparent;
}

@keyframes tip-move {
  0% {
    opacity: 0;
    transform: translateY(0);
  }
  15% {
    opacity: 1;
    transform: translateY(0);
  }
  20% {
    opacity: 1;
    transform: translateY(0);
  }
  80% {
    opacity: 1;
    transform: translateY(50%)
  }
  85% {
    opacity: 1;
    transform: translateY(50%)
  }
  100% {
    opacity: 0;
    transform: translateY(50%);
  }
}
</style>