<script setup lang="ts">
import router from './router';
import { RouterView } from 'vue-router'
import { useCurrentIndexStore } from './stores/currentIndex';
import { storeToRefs } from 'pinia';
import NavigationBar from './components/NavigationBar.vue';
import { watch } from 'vue';

const {getPath, adjustIndex} = useCurrentIndexStore()
const {currentIndex} = storeToRefs(useCurrentIndexStore())
let wheelBlocked = false

watch(currentIndex, () => {
  console.log("wow")
})

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
  <div class="scroll-tip"></div>
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

.scroll-tip {
  position: absolute;
  background-color: red;
  width: 100px;
  height: 50px;
  top: 80vh;
  left: 50vw;
}

header {
  position: absolute;
  width: 100vw;
  height: 10vmin;
  z-index: 10;
}

</style>
