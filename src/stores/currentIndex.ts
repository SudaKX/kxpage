import { defineStore } from 'pinia'
import { routeButtonData } from '@/router'

export const useCurrentIndexStore = defineStore('cIndex', () => {
  const maxIndex = routeButtonData.length - 1
  let currentIndex = 0
  function setIndex(index: number) {
    currentIndex = index
  }
  function adjustIndex(step: number): boolean {
    const temp = currentIndex + step
    if (temp <= maxIndex && temp >= 0) {
      currentIndex += step
      return true
    }
    return false
  }
  function getPath(): string {
    return routeButtonData[currentIndex].path
  }
  return { currentIndex, setIndex, adjustIndex, getPath }
})
