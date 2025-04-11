
/**
 * Written by Darksky
 */

const imageDataStorage: Map<string, ImageBitmap> = new Map();

export class ImageDisplayCanvas {

  identifierSet: Set<string>;
  bindCanvas: HTMLCanvasElement;
  bindContext: CanvasRenderingContext2D;

  constructor(canvas: HTMLCanvasElement) {
    this.identifierSet = new Set();
    this.bindCanvas = canvas;
    this.bindContext = canvas.getContext("2d") as CanvasRenderingContext2D;
  }

  hasImageData(identifier: string): boolean {
    return imageDataStorage.has(identifier);
  }
  setImageData(identifier: string, data: ImageBitmap): void {
    imageDataStorage.set(identifier, data);
    this.identifierSet.add(identifier);
  }

  clear(): void {
    console.log("clear");
  }

  setWait(): void {
    console.log("set wait");
  }
  changeImage(identifier: string): void {
    console.log(`change to ${identifier}`);
    const data = imageDataStorage.get(identifier);
    if (data) {
      this.bindContext.drawImage(data, 0, 0);
    }
  }

  dispose(): void {

  }
  clearImageData(): void {
    for (const identifier of this.identifierSet) {
      imageDataStorage.delete(identifier);
    }
  }
}

