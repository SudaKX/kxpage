
import { ref } from 'vue';
import { defineStore } from 'pinia';

export interface EventSpec {
  eventUUID: string
  eventTitle: string
  eventDescription: string
  eventHref: string
  eventTime: string
  imageHash?: string
}

export const useEventData = defineStore('eventData', () => {
  let events: EventSpec[] = [];
  const eventIndex = ref(-1);
  const eventLoaded = ref(false);
  const targetIndex = ref(-1);
  const allowChange = ref(true);
  function getEvents(): EventSpec[] {
    return events;
  }
  function setEvents(newEvents: EventSpec[]): void {
    eventLoaded.value = true;
    events = newEvents;
  }
  return { eventLoaded, getEvents, setEvents, eventIndex, allowChange, targetIndex };
})
