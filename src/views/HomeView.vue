<script setup lang="ts">
import FrameWrapper from '@/components/FrameWrapper.vue';
</script>

<template>
  <FrameWrapper>
    <div class="glass g-top"></div>
    <div class="glass g-down"></div>
    <div class="container">
      <div class="texts">
        <div>
          <h2>苏州大学</h2>
          <h3>计算机科学与技术学院</h3>
        </div>
        <div class="h-sep"></div>
        <h1>学生科技协会</h1>
      </div>
      <div class="background"></div>
    </div>
  </FrameWrapper>
</template>

<style lang="css" scoped>

.container {
  position: absolute;
  top: 0%;
  left: 0%;
  height: 100%;
  width: 100%;

  background-color: transparent;

  transition:
    scale 1.0s ease,
    opacity 1.0s ease;
}

.texts {
  position: absolute;
  top: 40%;
  height: 14%;
  left: 10%;
  background-color: var(--kx-dark-black0-half);
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 15px;
  color: white;

  transition: 
    transform 1.0s ease,
    opacity 1.0s ease;
}

.h-sep {
  position: relative;
  flex: none;
  background-color: var(--kx-dark-activate);
  height: 100%;
  width: 5px;
  margin-left: 10px;
  margin-right: 10px;
}

.background {
  position: absolute;
  translate: 10% 0%;
  top: 0%;
  height: 100%;
  width: 100%;
  background-position: center;
  background-image: 
    radial-gradient(closest-side, var(--kx-dark-activate), transparent);
  background-repeat: no-repeat;

  animation: 15s movement linear infinite;
  z-index: -1;
}

.glass {
  position: absolute;
  width: 100%;
  height: 10%;
  backdrop-filter: blur(50px);
  background-color: var(--kx-dark-black0-half);
  z-index: 1;
}

.glass.g-top {
  top: 0%;
}

.glass.g-down {
  bottom: 0%;
}

h1 {
  text-align: left;
  position: relative;
  display: block;
  color: white;
  font-size: 400%;
}

@keyframes movement {
  0%, 100% {
    background-size: 50vmax 50vmax;
    opacity: 0;
  }
  25% {
    background-size: 70vmax 70vmax;
    opacity: 0.8;
  }
  50% {
    background-size: 100vmax 100vmax;
    opacity: 1.0;
  }
  60% {
    background-size: 90vmax 90vmax;
    opacity: 0.9;
  }
  90% {
    background-size: 100vmax 100vmax;
    opacity: 0;
  }
}

/* Forward Enter */

.forward-enter-from .texts {
  opacity: 0;
  transform: translate(-20vw, 0);
}

/* Forward Leave */

.forward-leave-to .container {
  opacity: 0;
  scale: 1.2 1.2;
}

/* Rewind Enter */
.rewind-enter-from .container {
  opacity: 0.5;
  scale: 1.2 1.2;
}

</style>
