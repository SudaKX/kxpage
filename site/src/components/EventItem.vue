<template>
  <div class="top">
    <div class="time">{{ props.eventTime }}</div>
    <div class="text-warp" @click="jump" ref="text-wrap">
      <div class="text" :class="{ wrapped: textWrapped, active: textActivated }" ref="text">
        {{ props.eventTitle }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { useEventData } from '@/stores/eventData';
  import { onMounted, onUnmounted, ref, toRefs, useTemplateRef, watch } from 'vue';
  const { eventIndex, allowChange, targetIndex } = toRefs(useEventData());
  const textWrapper = useTemplateRef("text-wrap");
  const textContent = useTemplateRef("text");
  const textWrapped = ref(false);
  const textActivated = ref(false);
  const emits = defineEmits<{
    (e: "changeIndex", index: number): void
  }>();
  let resizing = false;

  const props = defineProps<{
    eventTime: string,
    eventTitle: string,
    index: number;
  }>();

  function updateTextWrap(): void {
    const wrapRect = textWrapper.value?.getBoundingClientRect() as DOMRect;
    const textRect = textContent.value?.getBoundingClientRect() as DOMRect;
    if (textRect.width >= wrapRect.width) {
      textWrapped.value = true;
    } else {
      textWrapped.value = false;
    }
  }

  const cancelIndexWatch = watch(targetIndex, (value) => {
    textActivated.value = value === props.index ? true : false;
  });

  function resizeHandler(): void {
    if (!resizing) {
      resizing = true;
      setTimeout(() => {
        updateTextWrap();
        resizing = false;
      }, 500);
    }
  }

  function jump(): void {
    if (allowChange.value && targetIndex.value != props.index) {
      targetIndex.value = props.index;
      emits("changeIndex", props.index);
    }
  }

  onMounted(() => {
    updateTextWrap();
    if (eventIndex.value == props.index) {
      textActivated.value = true;
    }
    window.addEventListener("resize", resizeHandler);
  });

  onUnmounted(() => {
    cancelIndexWatch();
    window.removeEventListener("resize", resizeHandler);
  });

</script>

<style scoped>
div.top {
  position: relative;
  width: 100%;
  height: 8cqh;
  margin-bottom: 3cqh;
  display: flex;
  flex-direction: column;
  border-bottom: 2px solid var(--kx-dark-neglect);

  div.time {
    pointer-events: none;
    width: fit-content;
    height: 30%;
    padding-left: 2%;
    padding-right: 2%;
    background-color: var(--kx-dark-activate);
    font-size: 1.6cqh;
    vertical-align: middle;
    margin-bottom: .4cqh;
  }

  div.text-warp {
    cursor: pointer;
    width: 100%;
    height: 60%;
    overflow: hidden;
    mask-image: linear-gradient(90deg, rgba(0, 0, 0, 1) 90%, transparent);

    div.text {
      position: absolute;
      width: max-content;
      font-size: 3cqh;
      color: var(--kx-dark-neglect-light);
      transition: color 200ms ease;
    }

    div.text.active {
      color: var(--kx-dark-white0);
    }
  }

  div.text-warp:hover {
    div.wrapped {
      animation: 8s linear 0s text-move;
    }

    div.text {
      color: var(--kx-dark-white0);
    }
  }
}

@keyframes text-move {

  0%,
  10% {
    translate: 0 0;
  }

  90% {
    translate: -100% 0;
    opacity: 1;
  }

  94% {
    translate: -100% 0;
    opacity: 0;
  }

  95% {
    translate: 0 0;
    opacity: 0;
  }

  100% {
    opacity: 1;
  }
}
</style>