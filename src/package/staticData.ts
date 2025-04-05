
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

interface StaticDataSpec {
  departments: DetailSpec[]
  points: InputSpec[]
}

async function loadJson(filePath: string): Promise<StaticDataSpec> {
  try {
    const response = await fetch(filePath);
    if (!response.ok) {
      throw new Error(`Failed to load JSON file: ${response.status} ${response.statusText}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`Error loading JSON file: ${error}`);
    throw error;
  }
}

const staticData = await loadJson("/data.json")

export const departmentDescription = staticData.departments;
export const pointsGraphConfig = staticData.points
