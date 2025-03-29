<template>
  <nav class="nav-bar">
    <NavigationButton
      v-for="(item, index) in routeButtonData"
      v-bind="item" :key="index"/>
  </nav>
  <div class="logo">

  </div>
</template>

<script setup lang="ts">
import NavigationButton from './NavigationButton.vue';
import { routeButtonData } from '@/router/index'


</script>

<style scoped>
.nav-bar {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  width: 100%;
  height: 100%;
}

.logo {
  position: absolute;
  background-color: blue;
  height: 100%;
  width: 200px;
}
</style>


