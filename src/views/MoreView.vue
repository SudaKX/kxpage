<template>
  <FrameWrapper>
    <div class="top-content">
      <MoreSectionCard v-bind="moreCardsDescription[0]" style="transition-delay: 1s;">
        <div class="qr-code-container">
          <img class="qr-code" src="/src/assets/images/qrcode.jpg" draggable="false" />
        </div>
      </MoreSectionCard>
      <MoreSectionCard v-bind="moreCardsDescription[1]" style="transition-delay: 1.1s;">
        <div class="pseudo-card">
          <img class="bili-avatar" src="/src/assets/images/bili-avatar.webp" alt="bili-avatar" draggable="false" />
          <div class="info-part">
            <div class="head-name">计算机爱好者协会</div>
            <div class="signature">苏州大学计科院社团的账号</div>
            <div class="follow-button" @click="jumpBilibili">前往</div>
          </div>
        </div>
      </MoreSectionCard>
      <MoreSectionCard v-bind="moreCardsDescription[2]" style="transition-delay: 1.2s;">
        <div class="contributor" ref="contributor">
          <div class="scroll-display" ref="scroll-container">
            <ContributeAvatar v-for="(value, idx) in contributorAvatars" :key="idx" v-bind="value"></ContributeAvatar>
          </div>
          <div class="text-display">
            以上排名不分先后。
          </div>
        </div>
      </MoreSectionCard>
      <MoreSectionCard v-bind="moreCardsDescription[3]" style="transition-delay: 1.3s;">
        <!-- 在这里干活 -->
        <div class="repos-container">
          <div class="repo-container">
            <div class="repo-item-container">
              <div class="repo-title-container">
                <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16"
                  data-view-component="true">
                  <path
                    d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z">
                  </path>
                </svg>
                <p class="repo-title" @click="jumpGithubFrontend()">kxpage</p>
                <div class="repo-subtitle-container">
                  <p class="repo-subtitle">前端</p>
                </div>
              </div>
              <div class="repo-description">测试</div>
              <div class="repo-extra-info-container">
                <div class="repo-languages">
                  <span class="repo-language">
                    <span class="repo-language-color-tip repo-language-ts"></span>
                    TypeScript
                  </span>
                  <span class="repo-language">
                    <span class="repo-language-color-tip repo-language-vue"></span>
                    Vue
                  </span>
                </div>
              </div>
            </div>
          </div>
          <div class="repo-container">
            <div class="repo-item-container">
              <div class="repo-title-container">
                <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16"
                  data-view-component="true">
                  <path
                    d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z">
                  </path>
                </svg>
                <p class="repo-title" @click="jumpGithubBackend()">kxpage-backend</p>
                <div class="repo-subtitle-container">
                  <p class="repo-subtitle">后端</p>
                </div>
              </div>
              <div class="repo-description">测试</div>
              <div class="repo-extra-info-container">
                <div class="repo-languages">
                  <span class="repo-language">
                    <span class="repo-language-color-tip repo-language-python"></span>
                    Python
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </MoreSectionCard>
    </div>
    <div class="background">
      <img v-for="idx in [1, 2, 3, 4]" :key="idx" class="bg-placeholder" src="/src/assets/images/moreBackground.svg"
        alt="placeholder" />
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

function jumpGithubBackend(): void {
  window.open("https://github.com/SudaKX/kxpage-backend");
}

function jumpGithubFrontend(): void {
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
    return;
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
      font-size: 1.5vmin;
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

  mask-image: linear-gradient(90deg, transparent, black 10%, black 90%, transparent);
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
    repeating-linear-gradient(135deg, transparent, transparent 20px,
      var(--kx-dark-neglect-half) 20px, var(--kx-dark-neglect-half) 40px);
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

  background-image: radial-gradient(circle at center,
      var(--kx-dark-activate) 80%, transparent);
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

  div.overlay>div.text {
    translate: -120% 0;
  }
}

.forward-enter-active {
  div.card-top {
    transition: translate 500ms ease;
  }

  div.overlay>div.text {
    transition: translate 500ms ease .9s;
  }
}

div.repos-container {
  position: absolute;

  top: 0;
  left: 5%;
  width: 90%;
  height: 100%;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  gap: 10px;

  overflow-y: auto;
}

div.repo-container {
  background-color: white;

  width: 90%;
  height: 100px;

  border: #D1D9E0 1px solid;
  border-radius: 4px;

  cursor: default;


  >div.repo-item-container {
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;

    >div.repo-title-container {
      display: flex;
      flex-direction: row;
      align-items: center;

      >p.repo-title {
        cursor: pointer;
        display: inline-block;
        margin-left: 8px;
        font-size: 14px;
        font-weight: 600;
        color: #0969DA;

        translate: 0 -2px;
      }

      >p.repo-title:hover {
        text-decoration: underline;
      }

      >div.repo-subtitle-container {
        border: #D1D9E0 1px solid;
        border-radius: 8px;
        margin-left: 5px;

        >p.repo-subtitle {
          margin: 1px 5px 1px 5px;
          font-size: 12px;
          color: #57606A;
        }
      }
    }

    >div.repo-description {
      margin-top: 4px;
      font-size: 14px;
      height: 16px;
      color: #57606A;
    }

    >div.repo-extra-info-container {
      margin-top: 8px;
      display: flex;
      flex-direction: row;
      align-items: center;

      >div.repo-languages {
        font-size: 12px;
        color: #57606A;
        gap: 16px;

        >span.repo-language {
          margin: 0 6px 0 0;

          >span.repo-language-color-tip {
            width: 12px;
            height: 12px;

            border-radius: 50%;
            display: inline-block;

            translate: 0 1px;
          }

          >span.repo-language-ts {
            background-color: #3178C6;
          }

          >span.repo-language-vue {
            background-color: #41B883;
          }

          >span.repo-language-python {
            background-color: #3572A5;
          }
        }
      }
    }
  }
}
</style>