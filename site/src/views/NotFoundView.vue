<template>
  <FrameWrapper>
    <div class="box" :style="boxStyle">
      <h1 class="title">404</h1>
      <h2 class="detail">你来到了一片荒漠，这里什么都没有。</h2>
      <h2 class="detail" v-if="show">吗？</h2>
    </div>
    <div class="button" v-if="buttonShow" @click="changeRoute">HERE</div>
  </FrameWrapper>
</template>

<script setup lang="ts">
import FrameWrapper from '@/components/FrameWrapper.vue';
import { computed, onMounted, onUnmounted, ref, watch } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const show = ref(false);
const buttonShow = ref(false);
const boxOffset = ref(-50);
const boxStyle = computed(() => {
  return `translate: -50% ${boxOffset.value}%;`;
});
const cancel = watch(boxOffset, (value) => {
  if (value < -300) {
    buttonShow.value = true;
    cancel();
  }
})

function changeRoute(): void {
  router.replace("/WGluZyB5dW4gQWxwaGEgdjE=");
}

function wheelHandler(ev: WheelEvent): void {
  if (ev.deltaY < 0) {
    boxOffset.value -= 5;
  }
}

onMounted(() => {
  setTimeout(() => {
    document.addEventListener("wheel", wheelHandler);
    show.value = true;
  }, 10000);
})

onUnmounted(() => {
  document.removeEventListener("wheel", wheelHandler);
})
</script>

<style scoped>
div.box {
  pointer-events: none;
  position: absolute;
  left: 50%;
  top: 50%;
  width: 64vmin;
  height: 40vmin;
  background-color: var(--kx-dark-neglect-light);
  translate: -50% -50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow: 10px 10px var(--kx-dark-neglect);
  transition: translate 200ms linear;

  h1.title {
    color: var(--kx-dark-white0-dark);
    font-size: 3vmax;
  }

  h2.detail {
    color: var(--kx-dark-white0-dark);
    font-size: 1vmax;
    margin-top: 1vmin;
  }
}

div.button {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 10vmin;
  background-color: var(--kx-dark-neglect-light);
  translate: -50% -50%;
  text-align: center;
  box-shadow: 10px 10px var(--kx-dark-neglect);
  color: var(--kx-dark-white0-dark);
  font-size: 1.2vmax;
  user-select: none;
}
</style>