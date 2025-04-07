<template>
  <FrameWrapper>
    <Transition name="load" :duration="400" mode="out-in">
      <div v-if="eventLoaded" class="container">
        <h1> Event View</h1>
      </div>
      <div v-else-if="fetchFailed" class="fail">
        <div class="err-icon">:(</div>
        <div class="err-title">加载该页面时遇到错误</div>
        <div class="err-content">
          {{ errorContent }}
        </div>
        <div class="err-tip">
          打开控制台以查看详细错误信息
        </div>
      </div>
      <div v-else class="loading">
        <div class="icon">
          <div class="scaler">
            <div class="tl block"></div>
            <div class="tr block"></div>
            <div class="br block"></div>
          </div>
          <div class="bl block full"></div>
        </div>
        <h1 class="title">加载中...</h1>
      </div>
    </Transition>
  </FrameWrapper>
</template>

<script setup lang="ts">
import FrameWrapper from '@/components/FrameWrapper.vue';
import { useEventData } from '@/stores/eventData';
import { onMounted, onUnmounted, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { school } from '@/proto/compiled';
import axios from 'axios';

const message = school.PBClass.create({ name: "hello" });
const buffer  = school.PBClass.encode(message).finish();
const decoded = school.PBClass.decode(buffer);

const { eventLoaded } = storeToRefs(useEventData());
const { getEvents, setEvents } = useEventData();
const fetchFailed = ref(false);
const errorContent = ref("");
let timeoutNumber: number | undefined = undefined;

onMounted(() => {
  timeoutNumber = setTimeout(async () => {
    try {
      timeoutNumber = undefined;
      if (!eventLoaded.value) {
        const response = await axios.get(
          "http://local111", {
            timeout: 10000
          }
        );
        setEvents([]);
        console.log(response);
      }
    } catch (error) {
      console.error(error);
      if (error instanceof Error)
        errorContent.value = error.toString();
      fetchFailed.value = true;
    }
  }, 2500);
});

onUnmounted(() => {
  if (timeoutNumber) clearTimeout(timeoutNumber);
})


</script>

<style scoped>
div.container {
  position: relative;
  height: 100%;
  width: 100%;
  background-color: green;
}

div.loading {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 64vmin;
  height: 40vmin;
  background-color: var(--kx-dark-neglect-light);
  translate: -50% -50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow: 10px 10px var(--kx-dark-neglect);

  .title {
    position: relative;
    pointer-events: none;
    color: var(--kx-dark-white0-half);
    width: 30%;
    text-align: justify;
    text-align-last: justify;
    font-size: 1vmax;
    margin-top: 2vmax;
  }

  .icon {
    position: relative;
    height: 10vmin;
    width: 10vmin;
    background-color: transparent;

    div.scaler {
      position: absolute;
      width: 100%;
      height: 100%;
      transform-origin: 5% 95%;
      scale: 0.4;
      animation: icon-scaler 3s linear infinite;
    }

    div.block {
      position: absolute;
      margin: 5%;
      height: 40%;
      width: 40%;
      background-color: transparent;
      border: 5px solid var(--kx-dark-white0-dark);
    }

    div.full {
      background-color: var(--kx-dark-white0-dark);
      border: none;
    }

    div.tl {
      animation: icon-tl 3s linear infinite;
    }

    div.bl {
      top: 50%;
    }

    div.tr {
      left: 50%;
      animation: icon-tr 3s linear infinite;
    }

    div.br {
      top: 50%;
      left: 50%;
      animation: icon-br 3s linear infinite;
    }
  }
}

@keyframes icon-scaler {
  0%, 80%, 100% {
    scale: 1;
    animation-timing-function: ease-in;
  }
  90% {
    scale: 0.4;
  }
  95% {
    scale: 0.4;
  }
}

@keyframes icon-tl {
  0% {
    translate: -100%;
    opacity: 0;
    animation-timing-function: ease;
  }
  20% {
    opacity: 1;
    translate: 0;
  }
  65% { background: transparent; }
  75% { background-color: var(--kx-dark-white0-dark); }
  90% { opacity: 1; background-color: var(--kx-dark-white0-dark); }
  92% { opacity: 0; }
  100% { opacity: 0; }
}

@keyframes icon-tr {
  0% {
    opacity: 0;
  }
  20% {
    translate: 0 -100%;
    opacity: 0;
    animation-timing-function: ease;
  }
  40% {
    translate: 0;
    opacity: 1;
  }
  65% { background: transparent; }
  75% { background-color: var(--kx-dark-white0-dark); }
  90% { opacity: 1; background-color: var(--kx-dark-white0-dark); }
  92% { opacity: 0; }
  100% { opacity: 0; }
}

@keyframes icon-br {
  0% {
    opacity: 0;
  }
  40% {
    translate: 100% 0;
    opacity: 0;
    animation-timing-function: ease;
  }
  60% {
    translate: 0;
    opacity: 1;
  }
  65% { background: transparent; }
  75% { background-color: var(--kx-dark-white0-dark); }
  90% { opacity: 1; background-color: var(--kx-dark-white0-dark); }
  92% { opacity: 0; }
  100% { opacity: 0; }
}

div.fail {
  position: absolute;
  pointer-events: none;
  left: 50%;
  top: 50%;
  width: 64vmin;
  height: 40vmin;
  background-color: var(--kx-dark-neglect-light);
  translate: -50% -50%;
  padding-left: 5vmin;
  padding-right: 5vmin;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  box-shadow: 10px 10px var(--kx-dark-neglect);
  color: var(--kx-dark-white0-dark);

  div.err-icon {
    font-size: 5vmax;
  }

  div.err-title {
    margin-top: 1vmin;
    font-size: 2vmax;
  }

  div.err-content {
    margin-top: 1vmin;
    font-size: 1vmax;
    background-color: var(--kx-dark-neglect);
    padding: 1vmin;
  }

  div.err-tip {
    margin-top: 1vmin;
    font-size: 0.6vmax;
  }

}

.forward-enter-from,
.rewind-enter-from {
  div.loading {
    opacity: 0;
  }
}

.forward-enter-active,
.rewind-enter-active {
  div.loading {
    transition:
      opacity 200ms ease-in-out 800ms;
  }
}

.load-leave-active {
  transition: opacity 200ms ease-in-out;
}

.load-enter-active {
  transition: opacity 200ms ease-in-out;
}

.load-enter-from {
  opacity: 0;
}

.load-leave-to {
  opacity: 0;
}

</style>
