<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <header>
    <div class="wrapper">
      <HelloWorld msg="You did it!" />

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>
  <div class="router-view">
    <RouterView v-slot="{ Component }">
        <Transition name="view">
          <component class="frame" :is="Component"/>
        </Transition>
    </RouterView>
  </div>
</template>

<style scoped>

.router-view {
  position: absolute;
  display: flex;
  flex-direction: row;
  top: 0px;
  left: 0px;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background-color: aliceblue;
  z-index: 0;
  align-items: center;
}

header {
  position: absolute;
  z-index: 1145;
  background-color: aquamarine;
}

.view-enter-active,
.view-leave-active {
  transition:
    opacity 2s ease,
    transform 2s ease;
}

.view-enter-from {
  transform: translate(100vw, 0);
  opacity: 0;
}

.view-leave-to {
  transform: translate(-100vw, 0);
  opacity: 0;
}

.frame {
  width: 100vw;
  height: 80vh;
  overflow: hidden;
  position: absolute;
}

</style>
