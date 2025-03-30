import { ref } from 'vue'
import { defineStore } from 'pinia'
import { routeButtonData } from '@/router'

export const useCurrentIndexStore = defineStore('cIndex', () => {
  const maxIndex = routeButtonData.length - 1
  const currentIndex = ref(0)
  function setIndex(index: number) {
    currentIndex.value = index
  }
  function adjustIndex(step: number): boolean {
    const temp = currentIndex.value + step
    if (temp <= maxIndex && temp >= 0) {
      currentIndex.value += step
      return true
    }
    return false
  }
  function getPath(): string {
    return routeButtonData[currentIndex.value].path
  }
  return { currentIndex, setIndex, adjustIndex, getPath }
})
