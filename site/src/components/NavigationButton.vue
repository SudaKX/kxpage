<template>
  <div>
    <RouterLink :to="props.path" class="link" :replace="true">
      <div class="title">{{ props.title }}</div>
      <div class="subtitle">{{ props.subtitle }}</div>
    </RouterLink>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  title: string
  subtitle: string
  path: string
}>()
</script>

<style scoped>
/* @font-face {
  font-family: "Oswald-Medium";
  src: url(https://github.com/googlefonts/OswaldFont/blob/main/fonts/ttf/Oswald-Medium.ttf);
} */

.link {
  display: block;
  margin-right: 50px;

  text-decoration: none;
  color: white;
  font-size: 2.2vmin;
  transition:
    color 0.5s;
}

.router-link-active.link {
  color: var(--kx-dark-activate);
}

.link:hover {
  color: var(--kx-dark-activate);
}

.title {
  font-family: "Oswald-Medium", sans-serif;
  font-weight: 900;
}

.subtitle {
  font-family: Arial, Helvetica, sans-serif;
  font-weight: 500;
}

</style>
