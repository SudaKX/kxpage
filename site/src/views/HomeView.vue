<script setup lang="ts">
import FrameWrapper from '@/components/FrameWrapper.vue';

function jumpVolunteer(): void {
  window.open("/volunteer");
}

</script>

<template>
  <FrameWrapper>
    <div class="glass g-top"></div>
    <div class="glass g-down"></div>
    <div class="container">
      <div class="title-container">
        <div class="texts">
          <div class="left-part">
            <h2>苏州大学</h2>
            <h3>计算机科学与技术学院</h3>
          </div>
          <div class="h-sep"></div>
          <h1>学生科技协会</h1>
        </div>
        <div class="jump-button" @click="jumpVolunteer">
          <div class="button-text">前往志愿者系统</div>
          <img class="button-icon" src="/src/assets/images/jump-icon.png" alt="jump-icon" draggable="false" />
        </div>
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
    opacity 1.0s ease,
    transform 1.0s ease;
}

div.title-container {
  position: absolute;
  top: 40%;
  left: 10%;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;

  >div.jump-button {
    position: relative;
    cursor: pointer;

    margin-top: 15px;
    padding: 5px 15px;

    display: flex;
    flex-direction: row;
    align-items: center;

    background-image: linear-gradient(90deg, var(--kx-dark-activate) 70%, transparent);
    background-repeat: no-repeat;
    background-size: 0 auto;
    background-position: left;

    transition:
      background-size 300ms ease .1s;

    >div.button-text {
      position: relative;

      font-size: 2vmin;
      margin-right: 10px;
      color: var(--kx-dark-white0);

      transition: color 300ms ease .1s;
    }

    >img.button-icon {
      position: relative;

      width: 2vmin;
      height: 2vmin;
      margin-right: 8vmin;

      object-position: center;
      object-fit: contain;

      transition: filter 300ms ease .1s;
    }
  }

  >div.jump-button:hover {
    background-size: 100% auto;

    >div.button-text {
      color: var(--kx-dark-white0-bright);
    }

    >img.button-icon {
      filter: invert(100%);
    }
  }
}

.texts {
  position: relative;

  display: flex;
  flex-direction: row;
  align-items: stretch;
  padding: 15px;
  color: white;

  >div.left-part {
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
}

.h-sep {
  position: relative;
  flex: none;
  background-color: var(--kx-dark-activate);
  width: 0.5vmax;
  margin-left: 1vmax;
  margin-right: 1vmax;
}

.background {
  position: absolute;
  translate: 0 0;
  top: 0;
  height: 100%;
  width: 115%;
  background-position: center;
  background-image:
    radial-gradient(closest-side, var(--kx-dark-activate), transparent);
  background-repeat: no-repeat;

  animation: 15s movement linear infinite;
  z-index: -2;
}

.glass {
  position: absolute;
  width: 100%;
  height: 10%;
  backdrop-filter: blur(25px);
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
  cursor: default;
  text-align: left;
  position: relative;
  display: block;
  color: white;
  font-size: 3vmax;
}

h2 {
  cursor: default;
  font-size: 1.5vmax;
}

h3 {
  cursor: default;
  font-size: 1vmax;
}

@keyframes movement {

  0%,
  100% {
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
    background-size: 105vmax 105vmax;
    opacity: 1.0;
  }

  85% {
    background-size: 80vmax 80vmax;
    opacity: 0;
  }
}

/* Forward Enter */

.forward-enter-from .container {
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
