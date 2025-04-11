
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
  function getEvents(): EventSpec[] {
    return events;
  }
  function setEvents(newEvents: EventSpec[]): void {
    eventLoaded.value = true;
    events = newEvents;
  }
  return { eventLoaded, getEvents, setEvents, eventIndex};
})
