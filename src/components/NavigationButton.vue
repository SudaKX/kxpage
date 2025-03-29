<template>
  <div>
    <RouterLink :to="props.path" class="link">
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
  background-color: black;
  margin-right: 50px;

  text-decoration: none;
  color: white;
  font-size: large;
  transition:
    color 0.5s,
    text-shadow 0.5s;
}

.router-link-active.link {
  color: blue;
}

.link:hover {
  color: blue;
  text-shadow: 1px 1px 2px green;
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
