<template>
  <div class="avatar">
    <div class="link-overlay" @click="jumpSite"></div>
    <img alt="avatar" :src="useSrcPath"/>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  path: string,
  href?: string
}>();
const useSrcPath = `/avatars/${props.path}`;

function jumpSite(): void {
  if (props.href) {
    window.open(props.href);
  }
}
</script>

<style scoped>
div.avatar {
  position: relative;
  box-shadow: 0 0 5px var(--kx-dark-neglect);
  height: 15cqh;
  width: 15cqh;
  border-radius: 15cqh;
  border: 3px var(--kx-dark-neglect) solid;
  overflow: hidden;
  margin-right: 1cqh;
  flex: none;

  >div.link-overlay {
    cursor: pointer;
    position: absolute;
    height: 100%;
    width: 100%;
    z-index: 1;
  }

  >img {
    position: absolute;
    height: 100%;
    width: 100%;
    object-position: center;
    object-fit: contain;
  }
}
</style>