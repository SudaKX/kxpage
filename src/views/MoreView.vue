<template>
  <FrameWrapper>
    <div class="top-content">
      <MoreSectionCard v-bind="moreCardsDescription[0]" style="transition-delay: 1s;">
        <div class="qr-code-container">
          <img class="qr-code" src="/src/assets/images/qrcode.jpg" draggable="false"/>
        </div>
      </MoreSectionCard>
      <MoreSectionCard v-bind="moreCardsDescription[1]" style="transition-delay: 1.1s;">
        <div class="pseudo-card">
          <img class="bili-avatar" src="/src/assets/images/bili-avatar.webp" alt="bili-avatar" draggable="false"/>
          <div class="info-part">
            <div class="head-name">计算机爱好者协会</div>
            <div class="signature">苏州大学计科院社团，旗...</div>
            <div class="follow-button" @click="jumpBilibili">+ 关注</div>
          </div>
        </div>
      </MoreSectionCard>
      <MoreSectionCard v-bind="moreCardsDescription[2]" style="transition-delay: 1.2s;">
        <div class="contributor" ref="contributor">
          <div class="scroll-display" ref="scroll-container">
            <ContributeAvatar v-for="(value, idx) in contributorAvatars"
              :key="idx" v-bind="value"></ContributeAvatar>
          </div>
          <div class="text-display">
            以上排名不分先后。
          </div>
        </div>
      </MoreSectionCard>
      <MoreSectionCard v-bind="moreCardsDescription[3]" style="transition-delay: 1.3s;">
        <div class="link-button" @click="jumpGithub">
          <div class="link-text">SudaKX/kxpage</div>
        </div>
      </MoreSectionCard>
    </div>
    <div class="background">
      <img v-for="idx in [1, 2, 3, 4]" :key="idx"
        class="bg-placeholder"
        src="/src/assets/images/moreBackground.svg"
        alt="placeholder"/>
    </div>
    <div class="overlay">
      <div class="text">MORE CONTENT</div>
    </div>
  </FrameWrapper>
</template>

<script setup lang="ts">
import FrameWrapper from '@/components/FrameWrapper.vue';
import MoreSectionCard from '@/components/MoreSectionCard.vue';
import ContributeAvatar from '@/components/ContributeAvatar.vue';
import { moreCardsDescription, contributorAvatars } from '@/package/staticData';
import { onMounted, onUnmounted, useTemplateRef, watchEffect, type WatchHandle } from 'vue';
  
function jumpGithub(): void {
  window.open("https://github.com/SudaKX/kxpage");
}

function jumpBilibili(): void {
  window.open("https://space.bilibili.com/371654507")
}

const avatarsListRef = useTemplateRef("scroll-container");
const outerContainerRef = useTemplateRef("contributor");
let avatarsList: HTMLDivElement;
let outerContainer: HTMLDivElement;
let watchHandler: WatchHandle;
let animationHandle: number = -1;
let lastAnimateTick: number = -1;
let listXPosition: number;
let listWidth: number;
let containerWidth: number;
const moveSpeedFactor: number = 0.1;

function rearrangeSize(): void {
  const oR = outerContainer.getBoundingClientRect();
  listWidth = Math.floor(avatarsList.getBoundingClientRect().width);
  containerWidth = Math.floor(oR.width);
  listXPosition = containerWidth;

  if (animationHandle > 0) {
    cancelAnimationFrame(animationHandle);
  }
  if (containerWidth >= listWidth) {
    const center = Math.floor((containerWidth - listWidth) / 2);
    avatarsList.style.translate = `${center}px 0`;
  } else {
    animationHandle = requestAnimationFrame(animationFrame);
  }
}

function animationFrame(timestamp: number): void {
  // first start
  if (lastAnimateTick < 0) {
    lastAnimateTick = timestamp;
    animationHandle = requestAnimationFrame(animationFrame);
    return ;
  }

  const delta = Math.floor(timestamp - lastAnimateTick);
  lastAnimateTick = timestamp;

  listXPosition -= containerWidth * moveSpeedFactor * delta / 1000;
  if (listXPosition < - listWidth) {
    listXPosition = containerWidth;
  }

  avatarsList.style.translate = `${Math.floor(listXPosition)}px 0`;

  animationHandle = requestAnimationFrame(animationFrame);
}

onMounted(() => {
  watchHandler = watchEffect(() => {
    if (avatarsListRef.value && outerContainerRef.value) {
      avatarsList = avatarsListRef.value;
      outerContainer = outerContainerRef.value;
      window.addEventListener("resize", rearrangeSize);
      rearrangeSize();
    }
  });
})

onUnmounted(() => {
  watchHandler();
  window.removeEventListener("resize", rearrangeSize);
  cancelAnimationFrame(animationHandle);
})
</script>

<style scoped>
div.qr-code-container {
  position: absolute;
  top: 5%;
  left: 5%;
  height: 90%;
  width: 90%;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  container-type: size;

  >img.qr-code {
    position: relative;
    width: 80cqw;
    height: 80cqw;

    object-fit: contain;
    object-position: center;

    filter: drop-shadow(0 0 5px var(--kx-dark-neglect));
  }
}

div.pseudo-card {
  position: absolute;

  left: 5%;
  top: 37%;
  width: 90%;
  height: 26%;

  background-color: var(--kx-dark-white0);
  box-shadow: 0 0 5px var(--kx-dark-neglect);

  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;

  padding: 0 10px;
  font-family: sans-serif;

  container-type: size;

  >img.bili-avatar {
    position: relative;
    height: 20cqw;
    width: 20cqw;

    flex: none;

    border-radius: 10cqw;
    border: 3px var(--kx-dark-neglect) solid;

    object-fit: contain;
    object-position: center;
  }

  >div.info-part {
    height: 100%;

    flex: none;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;

    >div.head-name {
      cursor: default;
      position: relative;
      font-size: 2.5vmin;
      font-weight: bold;
      color: var(--kx-dark-pink);
    }

    >div.signature {
      cursor: default;
      position: relative;
      font-size: 2vmin;
      font-weight: normal;
      color: var(--kx-dark-neglect-light);

      text-wrap: nowrap;
      overflow: hidden;
      width: 75cqw;
    }

    >div.follow-button {
      cursor: pointer;
      position: relative;
      font-size: 2vmin;
      font-weight: normal;

      width: 100%;
      background-color: var(--kx-dark-activate-weak);
      color: var(--kx-dark-white0);
      border-radius: 5px;

      margin-top: 5px;
      padding: 2px 0;
      text-align: center;

      transition: background-color 300ms ease;
    }

    >div.follow-button:hover {
      background-color: var(--kx-dark-activate);
    }
  }
}

div.contributor {
  position: absolute;

  top: 0;
  left: 5%;
  width: 90%;
  height: 100%;

  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;

  overflow: hidden;

  container-type: size;

  mask-image: linear-gradient(
    90deg, transparent, black 10%, black 90%, transparent);
  mask-mode: alpha;

  >div.scroll-display {
    position: relative;
    height: fit-content;
    width: fit-content;

    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    margin-bottom: 5px;
  }

  >div.text-display {
    position: relative;

    cursor: default;
    width: 100%;

    text-align: center;
    font-size: 2vmin;
    color: var(--kx-dark-white0-weak);
    background-color: var(--kx-dark-neglect-half);
  }
}

div.overlay {
  left: -1%;
  pointer-events: none;
  position: absolute;
  bottom: -1%;
  width: 102%;
  height: 14%;

  overflow: hidden;

  z-index: 3;

  div.text {
    position: absolute;
    left: 5%;
    font-size: 8vmin;
    font-family: 'Times New Roman', Times, serif;
    font-weight: bold;
    color: var(--kx-dark-neglect);
  }

}

div.top-content {
  position: absolute;
  height: 100%;
  width: 100%;

  display: flex;
  flex-direction: row;
  align-items: center;
}

div.background {
  position: absolute;
  height: 100%;
  width: 100%;

  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-evenly;

  background-image:
    repeating-linear-gradient(
      135deg, transparent, transparent 20px,
      var(--kx-dark-neglect-half) 20px, var(--kx-dark-neglect-half) 40px
    );
  background-size: 282.84px 282.84px;
  animation: 6s linear 0s infinite normal none bg-animation;

  z-index: -1;

  >img.bg-placeholder {
    filter: brightness(1.5);
  }
}

@keyframes bg-animation {
  0% {
    background-position-x: 0;
  }
  100% {
    background-position-x: 282.84px;
  }
}

div.link-button {
  position: absolute;
  cursor: pointer;

  height: 16%;
  width: 60%;
  left: 20%;
  top: 42%;

  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;

  background-image: radial-gradient(
    circle at center,
    var(--kx-dark-activate) 80%, transparent
  );
  background-color: var(--kx-dark-neglect-light-half);
  background-repeat: no-repeat;
  background-size: 0 0;
  background-position: center;

  filter: drop-shadow(0 0 5px var(--kx-dark-black0));

  transition:
    scale 300ms ease,
    background-size 300ms ease;

  >div.link-text {
    font-size: 2.5vmin;
    text-align: center;
    font-weight: normal;
    color: var(--kx-dark-white0);
  }
}

div.link-button:hover {
  scale: 1.15;
  background-size: 50vmin 50vmin;
}

.forward-enter-from {
  div.card-top {
    translate: 0 100%;
  }
  div.overlay >div.text {
    translate: -120% 0;
  }
}

.forward-enter-active {
  div.card-top {
    transition: translate 500ms ease;
  }
  div.overlay >div.text {
    transition: translate 500ms ease .9s;
  }
}
</style>