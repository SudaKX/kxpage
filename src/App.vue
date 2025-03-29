<script setup lang="ts">
import router from './router';
import { RouterView } from 'vue-router'
import { useCurrentIndexStore } from './stores/currentIndex';
import NavigationBar from './components/NavigationBar.vue';

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
      }, 1500);
    }
  }
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
        :duration="1500"
      >
        <component :is="Component"/>
      </Transition>
    </RouterView>
  </div>
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
  z-index: 0;
}

header {
  position: absolute;
  width: 100vw;
  height: 10vmin;
  z-index: 10;
}

</style>
