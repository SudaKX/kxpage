<template>
  <div class="contain">
    <div class="list animate">
      <div class="scroll-box" ref="sbBox">
        <div class="scroll-bar" ref="sbInner"></div>
      </div>
      <div class="scroll-contain" ref="scBox">
        <div class="scroll-content" ref="scInner">
          <EventItem ref="items" @changeIndex="indexChangeHandler"
            v-for="(obj, index) in listSpecs" :key="index" v-bind="obj">
          </EventItem>
        </div>
      </div>
    </div>
    <div class="swiper animate">
      <div class="display">
        <div class="image-container">
          <div class="image-err" v-if="errorImage">
            <h1 class="err-title">{{ errorTitle }}</h1>
            <h2 class="err-texts">{{ errorContent }}</h2>
          </div>
          <div class="image-mask" :class="imageMaskState">
            <h1 class="mask-texts">(NLink://Action) -> Loading . . .</h1>
          </div>
          <canvas class="image-canvas" ref="canvas"></canvas>
        </div>
        <div class="event-desc" :class="{hide: hideDescTexts}">
          {{ currentDesc }}
        </div>
        <div class="href-button" :class="{inactive: buttonInactive}" @click="jump">
          <div class="ch-title">了解更多</div>
          <div class="en-title">
            <div class="button-text">READ MORE</div>
            <svg class="arrow" viewBox="0 0 100 50">
              <polygon points="0,0 20,0 50,30 60,40 50,50" />
              <polygon points="80,0 100,0 70,30 60,20"/>
            </svg>
          </div>
        </div>
      </div>
    </div>
    <div class="bg-text">Events</div>
    <div class="bg-block bg-block-1 animate-bg"></div>
    <div class="bg-block bg-block-2 animate-bg"></div>
    <div class="event-bg" ></div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, type Reactive, reactive, ref, useTemplateRef, watch} from 'vue';
import EventItem from './EventItem.vue';
import { useEventData } from '@/stores/eventData';
import { VerticalScrollBar } from '@/package/scrollBar';
import { ImageDisplayCanvas } from '@/package/imageDisplay';
import axios from 'axios';
import { storeToRefs } from 'pinia';

interface ListItemSpec {
  eventTime: string;
  eventTitle: string;
  index: number;
}

const { getEvents } = useEventData();
const { eventIndex, allowChange } = storeToRefs(useEventData());
const listSpecs: Reactive<ListItemSpec[]> = reactive([]);
const sbBox = useTemplateRef("sbBox");
const sbInner = useTemplateRef("sbInner");
const scBox = useTemplateRef("scBox");
const scInner = useTemplateRef("scInner");
const items = useTemplateRef("items");
const displayCanvas = useTemplateRef("canvas");
const hideDescTexts = ref(false);
const buttonInactive = ref(true);
const errorImage = ref(true);
const errorTitle = ref("Error: No content.");
const errorContent = ref("null");
const imageMaskState = ref("");
const currentDesc = computed(() => {
  return getEvents()[eventIndex.value]?.eventDescription;
});
let sbManager: VerticalScrollBar | undefined ;
let imageDisplay: ImageDisplayCanvas | undefined;
let lastTimeoutNumber: number | undefined;

const cancelItemsLoad = watch(items, (value) => {
  if (value) {
    sbManager = new VerticalScrollBar(
      sbBox.value as HTMLElement, sbInner.value as HTMLElement,
      scBox.value as HTMLElement, scInner.value as HTMLElement
    );
    imageDisplay = new ImageDisplayCanvas(
      displayCanvas.value as HTMLCanvasElement
    );
    if (eventIndex.value >= 0) {
      const imageHash = getEvents()[eventIndex.value].imageHash;
      const eventHref = getEvents()[eventIndex.value].eventHref;
      if (imageHash) {
        const success = imageDisplay?.changeImage(imageHash);
        if (!success) {
          errorImage.value = true;
          errorTitle.value = "Error: No content.";
          errorContent.value = `Image data for ${imageHash} is empty.`;
        }
      } else {
        errorImage.value = true;
        errorTitle.value = "Error: No content.";
        errorContent.value = "No image data for current event."
      }
      if (!eventHref) {
        buttonInactive.value = true;
      }
    }
    cancelItemsLoad();
  }
});

async function indexChangeHandler(index: number): Promise<void> {
  const event = getEvents()[index];

  buttonInactive.value = true;
  imageMaskState.value = "at-mid";
  hideDescTexts.value = true;
  allowChange.value = false;
  let fail = false;

  if (event.imageHash) {
    if (!imageDisplay?.hasImageData(event.imageHash)) {
      try {
        const response = await axios.get("/api/images", {
          params: {h: event.imageHash},
          timeout: 10000, 
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          },
          responseType: "blob"
        });
        const blob = new Blob(
          [response.data], {type: response.headers['Content-Type'] as string}
        )
        const url = URL.createObjectURL(blob);
        const imageElement = document.createElement("img");
        const loadImage = (): Promise<HTMLImageElement> => {
          return new Promise((resolve, reject) => {
            imageElement.src = url;
            imageElement.onload = () => resolve(imageElement);
            imageElement.onerror = () => reject(new Error(`Fail to load ${event.imageHash}.`));
          });
        }
        const element = await loadImage();
        const imageBitmap = await window.createImageBitmap(
          element, 0, 0, element.width, element.height
        );
        URL.revokeObjectURL(url);
        imageDisplay?.setImageData(event.imageHash as string, imageBitmap);
        fail = false;
      } catch (e) {
        fail = true;
        errorTitle.value = "Error: unknown."
        errorContent.value = "null";
        if (e instanceof Error) {
          errorTitle.value = e.toString();
          errorContent.value = e.stack || "null";
        }
      }
    }
  } else {
    fail = true;
    errorTitle.value = "Error: No content.";
    errorContent.value = "No image data for current event."
  }

  lastTimeoutNumber = setTimeout(() => {
    errorImage.value = fail;
    eventIndex.value = index;
    buttonInactive.value = event.eventHref ? false : true;
    hideDescTexts.value = false;
    imageMaskState.value = "at-dest";
    if (event.imageHash) {
      imageDisplay?.changeImage(event.imageHash);
    }
    lastTimeoutNumber = setTimeout(() => {
      imageMaskState.value = "";
      allowChange.value = true;
      lastTimeoutNumber = undefined;
    }, 500);
  }, 500);
}

onMounted(() => {
  allowChange.value = true;
  const events = getEvents();
  if (eventIndex.value >= 0) {
    errorImage.value = false;
    buttonInactive.value = false;
  }
  events.forEach((value, index) => {
    listSpecs.push({
      eventTime: value.eventTime,
      eventTitle: value.eventTitle,
      index: index
    });
  });
});

onUnmounted(() => {
  sbManager?.dispose();
  if (lastTimeoutNumber) {
    clearTimeout(lastTimeoutNumber);
  }
})

function jump(): void {
  if (buttonInactive.value) return;
  window.open(getEvents()[eventIndex.value].eventHref, "_blank");
}

</script>

<style scoped>

div.contain {
  position: absolute;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  margin: auto;
  height: 100%;
  width: 100%;
}

div.event-bg {
  position: absolute;
  height: 100%;
  width: 100%;
  background-color: var(--kx-dark-neglect-light-half);
  mask-image: url("../assets/images/cutMask.png");
  mask-mode: luminance;
  mask-size: cover;
  mask-position: center;
  z-index: -4;
}

div.bg-text {
  pointer-events: none;
  position: absolute;
  color: var(--kx-dark-neglect-light);
  right: 3%;
  bottom: 3%;
  z-index: -3;
  font-size: 6vmax;
  font-family: 'Times New Roman', Times, serif;
  font-weight: bold;
}

div.bg-block {
  position: absolute;
  height: 200%;
  width: 200%;
  box-shadow: 0px 0px 10px black;
  backdrop-filter: blur(3px) brightness(50%);
}

div.bg-block-1 {
  translate: 30% -60%;
  rotate: 15deg;
  z-index: -1;
}

div.bg-block-2 {
  translate: -29% 58%;
  rotate: 40deg;
  z-index: -2;
}

div.swiper {
  position: relative;
  height: 100%;
  width: 50vmax;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  container-type: size;

  div.display {
    position: relative;
    height: 75cqmin;
    width: 100cqmin;

    div.image-container {
      position: absolute;
      top: 15%;
      left: 5%;
      width: 86.4%;
      height: 64.8%;
      overflow: hidden;

      div.image-err {
        position: absolute;
        width: 100%;
        height: 100%;
        padding: 5%;
        background-color: var(--kx-dark-white0-dark);
        z-index: 1;
        
        h1.err-title {
          font-size: 3.5cqmin;
        }
        h2.err-texts {
          font-size: 1.5cqmin;
          white-space: pre-line;
          font-weight: normal;
        }
      }

      div.image-mask {
        position: absolute;
        display: flex;
        align-items: center;
        width: 100%;
        height: 100%;
        background-color: var(--kx-dark-neglect-light);
        translate: 0 -110%;
        z-index: 2;

        h1.mask-texts {
          display: block;
          margin: 10%;
          font-family: 'Consolas', monospace;
          font-size: 3cqmin;
          color: var(--kx-dark-white0-dark);
          white-space: pre-line;
        }
      }

      div.image-mask.at-mid {
        transition: translate 500ms ease;
        translate: 0 0;
      }

      div.image-mask.at-dest {
        transition: translate 500ms ease;
        translate: 0 100%;
      }

      canvas.image-canvas {
        position: absolute;
        width: 100%;
        height: 100%;
      }
    }

    div.event-desc {
      pointer-events: none;
      position: absolute;
      right: 0%;
      bottom: 25%;
      width: 60%;
      height: 20%;
      background-color: var(--kx-dark-neglect-half);
      backdrop-filter: blur(3px);
      transition: opacity 500ms ease;
      font-size: 2cqmin;
      color: var(--kx-dark-white0-3qua);
      padding: 2cqmin;
      transition: color 500ms ease;
    }

    div.event-desc.hide {
      color: transparent;
    }

    div.href-button {
      cursor: pointer;
      position: absolute;
      bottom: 15%;
      right: 7%;
      height: 15%;
      width: 15%;
      background-color: var(--kx-dark-activate);
      transition: background-color 300ms ease;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-evenly;

      div.ch-title {
        pointer-events: none;
        position: relative;
        width: 90%;
        margin: 5% 5% 0 5%;
        color: var(--kx-dark-black0);
        font-size: 3.2cqmin;
        font-family: Arial, Helvetica, sans-serif;
        font-weight: bold;
      }

      div.en-title {
        position: relative;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        height: 50%;
        width: 90%;
        margin: 0% 3% 5% 7%;
        div.button-text {
          pointer-events: none;
          position: relative;
          font-size: 1.5cqmin;
          font-weight: bold;
          width: min-content;
          flex: none;
        }

        svg.arrow {
          width: 25%;
          rotate: -90deg;
        }
      }
    }

    div.href-button:hover {
      background-color: var(--kx-dark-white0);
    }

    div.href-button.inactive {
      background-color: var(--kx-dark-neglect);
    }
  }
}

div.list {
  position: relative;
  height: 100%;
  width: 25%;
  display: flex;
  flex-direction: row;
  align-items: center;

  div.scroll-box {
    position: relative;
    height: 70%;
    width: 4%;
    border: 2px solid var(--kx-dark-neglect);
    overflow: hidden;
    transition: border-color 200ms ease;

    div.scroll-bar {
      position: absolute;
      width: 76%;
      left: 12%;
      background-color: var(--kx-dark-neglect);
      transition: background-color 200ms ease;
      border-top: 1px solid var(--kx-dark-black0);
      border-bottom: 1px solid var(--kx-dark-black0);
      transition:
        translate 200ms ease,
        background-color 200ms ease;
    }
  }

  div.scroll-box.inactive {
    border-color: var(--kx-dark-neglect-half);
    div.scroll-bar {
      background-color: transparent;
    }
  }

  div.scroll-box.semi-hover {
    border-color: var(--kx-dark-neglect);

    div.scroll-bar {
      background-color: var(--kx-dark-neglect-light);
    }
  }

  div.scroll-box.hover {
    border-color: var(--kx-dark-neglect-light);

    div.scroll-bar {
      background-color: var(--kx-dark-white0-dark);
    }
  }

  div.scroll-box.pressed {
    border-color: var(--kx-dark-neglect-light);

    div.scroll-bar {
      background-color: var(--kx-dark-activate);
      transition: background-color 200ms ease;
    }
  }

  div.scroll-contain {
    position: relative;
    container-type: normal;
    height: 70%;
    width: 80%;
    padding-left: 7%;
    overflow: hidden;
    mask-image: linear-gradient(black 95%, transparent);

    div.scroll-content {
      position: relative;
      width: 100%;
      display: flex;
      flex-direction: column;
      transition: translate 200ms ease;
    }
  }

  div.scroll-contain.pressed {
    div.scroll-content {
      transition: none;
    }
  }
}

</style>