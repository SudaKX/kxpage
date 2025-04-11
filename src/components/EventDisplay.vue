<template>
  <div class="contain">
    <div class="list">
      <div class="scroll-box" ref="sbBox">
        <div class="scroll-bar" ref="sbInner"></div>
      </div>
      <div class="scroll-contain" ref="scBox">
        <div class="scroll-content" ref="scInner">
          <EventItem ref="items"
            v-for="(obj, index) in listSpecs" :key="index" v-bind="obj">
          </EventItem>
        </div>
      </div>
    </div>
    <div class="swiper">
      <div class="display">
        <canvas class="image-canvas" ref="canvas"></canvas>
        <div class="event-desc">
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
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, type Reactive, reactive, ref, toRefs, useTemplateRef, watch} from 'vue';
import EventItem from './EventItem.vue';
import { useEventData } from '@/stores/eventData';
import { VerticalScrollBar } from '@/package/scrollBar';
import { ImageDisplayCanvas } from '@/package/imageDisplay';
import axios from 'axios';

interface ListItemSpec {
  eventTime: string;
  eventTitle: string;
  index: number;
}

const { getEvents } = useEventData();
const { eventIndex } = toRefs(useEventData());
const listSpecs: Reactive<ListItemSpec[]> = reactive([]);
const sbBox = useTemplateRef("sbBox");
const sbInner = useTemplateRef("sbInner");
const scBox = useTemplateRef("scBox");
const scInner = useTemplateRef("scInner");
const items = useTemplateRef("items");
const displayCanvas = useTemplateRef("canvas");
const buttonInactive = ref(true);
const currentDesc = computed(() => {
  return getEvents()[eventIndex.value]?.eventDescription;
});
let sbManager: VerticalScrollBar | undefined ;
let imageDisplay: ImageDisplayCanvas | undefined;

const cancelItemsLoad = watch(items, (value) => {
  if (value) {
    sbManager = new VerticalScrollBar(
      sbBox.value as HTMLElement, sbInner.value as HTMLElement,
      scBox.value as HTMLElement, scInner.value as HTMLElement
    );
    imageDisplay = new ImageDisplayCanvas(
      displayCanvas.value as HTMLCanvasElement
    );
    cancelItemsLoad();
  }
});

const cancelEventIndexWatch = watch(eventIndex, (value) => {
  const event = getEvents()[value];
  buttonInactive.value = false;
  if (!imageDisplay) return ;
  if (event.imageHash) {
    if (imageDisplay.hasImageData(event.imageHash)) {
      imageDisplay.changeImage(event.imageHash);
    } else {
      imageDisplay.setWait();
      axios.get("http://127.0.0.1:8000/api/images", {
        params: {h: event.imageHash},
        timeout: 10000, 
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        },
        responseType: "blob"
      }).then((response) => {
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
        loadImage().then((element) => {
          window.createImageBitmap(
            element, 0, 0, element.width, element.height
          ).then((imageBitmap) => {
            URL.revokeObjectURL(url);
            imageDisplay?.setImageData(event.imageHash as string, imageBitmap);
            imageDisplay?.changeImage(event.imageHash as string);
          });
        });
      })
    }
  }
});

onMounted(() => {
  if (eventIndex.value >= 0) {
    buttonInactive.value = false;
  }
  const events = getEvents();
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
  imageDisplay?.dispose();
  cancelEventIndexWatch();
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

    canvas.image-canvas {
      position: absolute;
      top: 15%;
      left: 5%;
      width: 86.4%;
      height: 64.8%;
      background-color: aquamarine;
    }

    div.event-desc {
      position: absolute;
      right: 0%;
      bottom: 25%;
      width: 60%;
      height: 20%;
      background-color: var(--kx-dark-neglect-half);
      backdrop-filter: blur(3px);
      transition: opacity 500ms ease;
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
        margin: 0% 5% 5% 5%;
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