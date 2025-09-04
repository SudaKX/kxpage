<template>
  <div class="card-top" ref="card-top">
    <div class="vfx-overlay"></div>
    <div class="vfx-highlight" :style="useBGImage"></div>
    <div class="image-container">
      <img class="card-bg" :src="imageUrl" alt="card-background" draggable="false"/>
    </div>
    <div class="slot-container">
      <slot></slot>
    </div>
    <div class="title-container">
      <div class="top-part" ref="top-part" style="bottom: 0;">
        <div class="top-title">
          <img class="card-icon" alt="card-icon" :src="iconUrl"/>
          <div class="top-title-content">{{ useTitle }}</div>
        </div>
        <div class="divide-line"></div>
      </div>
      <div class="bottom-part" ref="bottom-part" style="height: 0;">
        <div class="sub-title" ref="subtitle">
          {{ useSubTitle }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, useTemplateRef, watchEffect, type WatchHandle } from 'vue';

// component props
const props = defineProps<{
  name: string,
  color: string,
  title?: string,
  subtitle?: string
}>();

// build resource urls
const imageUrl = `/more/${props.name}.jpg`;
const iconUrl = `/more/icon/${props.name}.png`;
const useTitle = props.title || "Title";
const useSubTitle = props.subtitle || "Subtitle";
const useBGImage = `background-image: linear-gradient(transparent 40%, ${props.color});`;

// positioning
let bottomDistance = 0;
let subTitle: HTMLDivElement;
let topPart: HTMLDivElement;
let cardContainer: HTMLDivElement;
let bottomPart: HTMLDivElement;

// template ref
const topPartRef = useTemplateRef("top-part");
const subTitleRef = useTemplateRef("subtitle");
const cardTopRef = useTemplateRef("card-top");
const bottomPartRef = useTemplateRef("bottom-part");
let watchHandler: WatchHandle;

function rearrangeSize(): void {
  bottomDistance = subTitle.getBoundingClientRect().height;
}

// onMounted
onMounted(() => {
  watchHandler = watchEffect(() => {
    if (topPartRef.value && subTitleRef.value && cardTopRef.value && bottomPartRef.value) {
      subTitle = subTitleRef.value;
      bottomDistance = subTitle.getBoundingClientRect().height;
      topPart = topPartRef.value;
      cardContainer = cardTopRef.value;
      bottomPart = bottomPartRef.value;
      
      cardContainer.addEventListener("mouseenter", () => {
        topPart.style.bottom = `${bottomDistance}px`;
        bottomPart.style.height = `${bottomDistance}px`;
      });

      cardContainer.addEventListener("mouseleave", () => {
        topPart.style.bottom = "0";
        bottomPart.style.height = "0";
      });

      window.addEventListener("resize", rearrangeSize);
    }
  })
})

onUnmounted(() => {
  watchHandler();
  window.removeEventListener("resize", rearrangeSize);
})

</script>

<style scoped>

div.card-top {
  position: relative;
  height: 100%;
  width: 25%;
  background-color: var(--kx-dark-black0);
}

div.vfx-overlay {
  position: absolute;
  pointer-events: none;
  height: 100%;
  width: 100%;

  background-image:
    linear-gradient(0deg, #000, transparent 40%),
    linear-gradient(0deg, #000, transparent 30%),
    linear-gradient(180deg, #000, rgba(0, 0, 0, .6) 10%, transparent 30%),
    linear-gradient(90deg, rgba(0, 0, 0, .7), transparent 3rem);

  z-index: 2;
}

div.vfx-highlight {
  position: absolute;
  pointer-events: none;

  width: 100%;
  height: 100%;

  opacity: 0;
  transition: opacity 300ms ease;

  z-index: 1;
}

div.image-container {
  position: absolute;
  height: 95%;
  width: 100%;

  overflow: hidden;

  img {
    position: absolute;
    height: 100%;
    width: 100%;

    transition: scale 300ms ease;
    object-position: center;
    object-fit: cover;
  }

  transition: filter 300ms ease;
  filter: grayscale(0.8);
}

div.title-container {
  position: absolute;
  pointer-events: none;

  height: 30%;
  width: 100%;
  top: 55%;

  z-index: 3;

  >div.top-part {
    position: absolute;
    pointer-events: none;

    width: 90%;
    left: 10%;
    height: 30%;

    transition: bottom 300ms ease;

    >div.top-title {
      position: relative;
      pointer-events: none;
      width: 100%;
      height: 80%;
      top: 0;

      display: flex;
      flex-direction: row;

      align-items: center;

      filter: drop-shadow(0 0 0.3rem black);

      >img.card-icon {
        height: 45%;
        object-position: center;
        object-fit: contain;
      }
      >div.top-title-content {
        margin-left: 5%;
        color: var(--kx-dark-white0);
        font-size: 3vmin;
      }
    }

    >div.divide-line {
      position: relative;
      pointer-events: none;

      bottom: 0;
      width: 0;
      height: 5%;
      background-color: var(--kx-dark-activate);

      transition: width 300ms ease;
      box-shadow: 0 0 5px black;
    }
  }

  >div.bottom-part {
    position: absolute;
    pointer-events: none;
    width: 80%;
    left: 10%;
    bottom: 0;

    overflow: hidden;

    transition: height 300ms ease;

    >div.sub-title {
      position: absolute;
      pointer-events: none;

      width: 100%;

      font-size: 2vmin;
      color: var(--kx-dark-white0-dark);
    }
  }
}

div.slot-container {
  position: absolute;

  top: 15%;
  left: 5%;
  height: 50%;
  width: 90%;

  opacity: 0;
  transition: opacity 300ms ease;

  z-index: 2;
}

div.card-top:hover {
  img.card-bg {
    scale: 1.1;
  }
  div.image-container {
    filter: grayscale(0);
  }
  div.title-container
  >div.top-part {
    bottom: 70%;

    >div.divide-line {
      width: 75%;
    }
  }
  >div.slot-container {
    opacity: 1;
  }
  >div.vfx-highlight {
    opacity: 1;
  }
}

</style>