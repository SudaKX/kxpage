<script setup lang="ts">
import router from './router';
import { RouterView } from 'vue-router'
import { useCurrentIndexStore } from './stores/currentIndex';
import NavigationBar from './components/NavigationBar.vue';
import ScrollArrow from './components/ScrollArrow.vue';
import { loadImages } from './package/points.ts';
import { onMounted } from 'vue';

const {getPath, adjustIndex} = useCurrentIndexStore()
let wheelBlocked = false

document.addEventListener('wheel', (ev) => {
  if (!wheelBlocked) {
    const step = ev.deltaY > 0 ? 1 : -1
    if (adjustIndex(step)) {
      wheelBlocked = true
      router.replace(getPath())
      setTimeout(() => {
        wheelBlocked = false
      }, 1000);
    }
  }
})

onMounted(async () => {
  await loadImages([
    {
      imagePath: "/xh-r.png",
      revert: true,
      offsetX: 500
    },
    {
      imagePath: "/xh-r.png",
      revert: false,
      scaleX: 0.5,
      scaleY: 0.5,
      offsetX: -500
    }
  ])
})

</script>

<template>
  <header>
    <NavigationBar></NavigationBar>
  </header>
  <div class="router-view">
    <RouterView v-slot="{ Component, route }">
      <Transition
        :name="(route.meta.transition as string) || 'forward'"
        :duration="1000"
      >
        <component :is="Component"/>
      </Transition>
    </RouterView>
  </div>
  <ScrollArrow></ScrollArrow>
</template>

<style scoped>

.router-view {
  position: absolute;
  display: flex;
  flex-direction: row;
  align-items: center;
  top: 0px;
  left: 0px;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

header {
  position: absolute;
  width: 100vw;
  height: 10vmin;
  z-index: 10;
}

</style>
