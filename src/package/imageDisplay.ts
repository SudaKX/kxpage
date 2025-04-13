
/**
 * Written by Darksky
 */

const imageDataStorage: Map<string, ImageBitmap> = new Map();

export class ImageDisplayCanvas {

  identifierSet: Set<string>;
  bindCanvas: HTMLCanvasElement;
  bindContext: CanvasRenderingContext2D;
  canvasHeight: number;
  canvasWidth: number;

  constructor(
    canvas: HTMLCanvasElement,
    canvasHeight: number = 1080,
    canvasWidth: number = 1920
  ) {
    this.identifierSet = new Set();
    canvas.height = canvasHeight;
    canvas.width = canvasWidth;
    this.canvasHeight = canvasHeight;
    this.canvasWidth = canvasWidth;
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

  changeImage(identifier: string): boolean {
    this.bindContext.clearRect(0, 0, this.canvasWidth, this.canvasHeight);
    const data = imageDataStorage.get(identifier);
    if (data) {
      const widthScaler = this.canvasWidth / data.width;
      const heightScaler = this.canvasHeight / data.height;
      const Scaler = Math.min(widthScaler, heightScaler);
      const drawHeight = Math.floor(Scaler * data.height);
      const drawWidth = Math.floor(Scaler * data.width);
      const left = Math.floor((this.canvasWidth - drawWidth) / 2);
      const top = Math.floor((this.canvasHeight - drawHeight) / 2);
      this.bindContext.drawImage(data, left, top, drawWidth, drawHeight);
      return true;
    }
    return false;
  }

  clearImageData(): void {
    for (const identifier of this.identifierSet) {
      imageDataStorage.delete(identifier);
    }
  }
}

