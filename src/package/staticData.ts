
interface DetailSpec {
  deptName: string
  deptEngName: string
  deptIntroduction: string
  offsetX?: number
  offsetY?: number
}

interface InputSpec {
  imagePath: string
  revert?: boolean
  alphaThreshold?: number
  brightnessThreshold?: number
  scaleX?: number
  scaleY?: number
  offsetX?: number
  offsetY?: number
}

interface CardDescription {
  color: string
  name: string
  title?: string
  subtitle?: string
}

interface AvatarDescription {
  path: string
  href?: string
}

interface StaticDataSpec {
  departments: DetailSpec[]
  points: InputSpec[]
  moreCards: CardDescription[]
  contributors: AvatarDescription[]
}

import jsonUrl from '@/assets/data.json';

const staticData = jsonUrl as StaticDataSpec;

export const departmentDescription = staticData.departments;
export const pointsGraphConfig = staticData.points;
export const moreCardsDescription = staticData.moreCards;
export const contributorAvatars = staticData.contributors;