
import { ref } from 'vue';
import { defineStore } from 'pinia';

interface EventSpec {
  eventName: string
  eventContent: string
}

export const useEventData = defineStore('eventData', () => {
  let events: EventSpec[] = [];
  const eventLoaded = ref(false);
  function getEvents(): EventSpec[] {
    return events;
  }
  function setEvents(newEvents: EventSpec[]): void {
    eventLoaded.value = true;
    events = newEvents;
  }
  return { eventLoaded, getEvents, setEvents };
})
