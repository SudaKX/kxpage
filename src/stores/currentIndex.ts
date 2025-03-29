import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useCurrentIndexStore = defineStore('cIndex', () => {
  const currentIndex = ref(0)
  function set(index: number) {
    currentIndex.value = index
  }
  return { currentIndex, set }
})
