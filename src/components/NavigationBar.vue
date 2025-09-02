<template>
  <nav class="nav-bar">
    <NavigationButton v-for="(item, index) in routeButtonData" v-bind="item" :key="index" />
  </nav>
  <img class="logo" src="@/assets/images/kx_icon.png">
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
  background-image:
    linear-gradient(var(--kx-dark-black0-half), transparent);
}

.logo {
  position: absolute;
  height: 100%;
  padding: 15px;
  padding-left: 50px;
}
</style>
