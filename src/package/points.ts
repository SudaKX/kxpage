
/**
 * Written by Darksky
 */

interface ImageInfo {
  imagePoints: PointSpec[],
  height: number,
  width: number
}

interface PointSpec {
  originX: number
  originY: number
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

let previousTimestamp: number | undefined
let imageLoaded: boolean = false
let bindCtx: CanvasRenderingContext2D | null = null
let cbNumber: number
let currentIndex: number = 0
let imageListSize: number
let leftOffset: number
let topOffset: number
let mouseX: number
let mouseY: number
let revertFlag: number
const imageInfos: ImageInfo[] = []
let currentPoints: Point[] = []

export const config = {
  brightnessThreshold: 170,
  alphaThreshold: 20,
  sampleStep: 5,
  fillR: 150,
  fillG: 150,
  fillB: 150,
  fillA: 0.6,
  alphaDuration: 500,
  particleSize: 2,
  distributeDistance: 100,
  offsetX: 0,
  offsetY: 0,
  ellipse: 0.0001,
  returnFactor: 0.6,
  pushFactor: 60000,
  maxPushForce: 200,
  minPushForce: 8,
  frictionFactor: 0.8,
  activationDelay: 1000,
  mouseScale: 1.0,
}

class Point {
  x: number
  y: number
  fx: number
  fy: number
  vx: number
  vy: number

  alpha: number
  targetAlpha: number
  alphaTransSpeed: number
  alphaDuration: number
  disappearFlag: boolean

  constructor(fixed_x: number, fixed_y: number) {

    this.x = fixed_x
    this.y = fixed_y
    this.fx = fixed_x
    this.fy = fixed_y
    this.vx = 0.0
    this.vy = 0.0

    this.alpha = 0.0
    this.targetAlpha = 0.0
    this.alphaTransSpeed = 0.0
    this.alphaDuration = 0
    this.disappearFlag = false
  }

  clear(ctx: CanvasRenderingContext2D): void {
    const length = Math.floor(config.particleSize / 2)
    ctx.clearRect(
      Math.floor(this.x) + leftOffset - length,
      Math.floor(this.y) + topOffset - length,
      length * 2, length * 2
    )
  }

  draw(ctx: CanvasRenderingContext2D): void {
    ctx.fillStyle = `rgba(
      ${config.fillR},
      ${config.fillG},
      ${config.fillB},
      ${this.alpha}
    )`
    ctx.beginPath();
    ctx.arc(
      Math.floor(this.x) + leftOffset,
      Math.floor(this.y) + topOffset,
      Math.floor(config.particleSize / 2),
      0, Math.PI * 2
    );
    ctx.fill();
  }

  appear(): void {
    this.disappearFlag = false
    this.targetAlpha = config.fillA
    this.alphaDuration = config.alphaDuration
    this.alphaTransSpeed = (this.targetAlpha - this.alpha) / config.alphaDuration
  }

  disappear(): void {
    this.disappearFlag = true
    this.targetAlpha = 0.0
    this.alphaDuration = config.alphaDuration
    this.alphaTransSpeed = (this.targetAlpha - this.alpha) / config.alphaDuration
  }

  cancelDisappear(): void {
    this.disappearFlag = false
    this.alphaDuration = 0
    this.alpha = config.fillA
  }

  vanished(): boolean {
    return (this.disappearFlag && (this.alphaDuration <= 0)) ? true : false
  }

  update(delta: number): void {
    // update alpha
    if (this.alphaDuration > 0) {
      this.alpha += this.alphaTransSpeed * delta
      this.alphaDuration -= delta
    }

    // apply offset
    const originX = this.fx + config.offsetX
    const originY = this.fy + config.offsetY
    
    let dx = originX - this.x
    let dy = originY - this.y

    this.vx += (Math.abs(dx) < config.ellipse ? 0 : dx) * config.returnFactor
    this.vy += (Math.abs(dy) < config.ellipse ? 0 : dy) * config.returnFactor

    // mouse interaction
    dx = mouseX - this.x
    dy = mouseY - this.y

    dx = Math.abs(dx) < config.ellipse ? 0 : dx
    dy = Math.abs(dy) < config.ellipse ? 0 : dy

    const square = (dx * dx) + (dy * dy)
    
    if (square > config.ellipse) {
      const force = Math.max(
        Math.min(config.pushFactor / square, config.maxPushForce),
        config.minPushForce
      )
      const distance = Math.sqrt(square)

      this.vx += dx / distance * force * revertFlag
      this.vy += dy / distance * force * revertFlag
    }

    // compute movement
    this.vx *= config.frictionFactor
    this.vy *= config.frictionFactor
    
    this.x += this.vx * delta / 1000
    this.y += this.vy * delta / 1000

  }

  randomPointSpec(maxRadius: number): PointSpec {
    const angle = Math.random() * 2 * Math.PI
    const distance = Math.random() * maxRadius
    return {
      originX: this.fx + Math.sin(angle) * distance,
      originY: this.fy + Math.cos(angle) * distance
    }
  }

  applyPosition(spec: PointSpec): void {
    this.x = spec.originX
    this.y = spec.originY
  }

  applyOrigin(spec: PointSpec): void {
    this.fx = spec.originX
    this.fy = spec.originY
  }

}

function singleFrame(timestamp: number): void {
  if (bindCtx) {
    cbNumber = requestAnimationFrame(singleFrame)

    if (previousTimestamp === undefined) {
      previousTimestamp = timestamp
      return undefined
    }

    const delta = Math.floor(timestamp - previousTimestamp)
    previousTimestamp = timestamp

    const nextPoints: Point[] = []
    for (const point of currentPoints) {
      point.clear(bindCtx)
      point.update(delta)

      if (!point.vanished()) {
        nextPoints.push(point)
        point.draw(bindCtx)
      }
    }
    
    currentPoints = nextPoints
  }
}

function changeImage(): void {
  if (!bindCtx) return

  const newPoints = imageInfos[currentIndex].imagePoints
  const commonSize = Math.min(newPoints.length, currentPoints.length)

  randomShuffle(newPoints)

  // keep common points - change point
  for (let index = 0; index < commonSize; ++index) {
    const spec = newPoints[index]
    currentPoints[index].cancelDisappear()
    currentPoints[index].applyOrigin(spec)
  }
  // disappear
  for (let index = commonSize; index < currentPoints.length; ++index) {
    const point = currentPoints[index]
    const spec = point.randomPointSpec(config.distributeDistance)
    point.applyOrigin(spec)
    point.disappear()
  }
  // append
  for (let index = commonSize; index < newPoints.length; ++index) {
    const spec = newPoints[index]
    const point = new Point(spec.originX, spec.originY)
    const randomSpec = point.randomPointSpec(config.distributeDistance)
    point.appear()
    point.applyPosition(randomSpec)
    currentPoints.push(point)
  }
}

function randomShuffle<T>(arr: Array<T>, start: number = 0, end: number = arr.length - 1): Array<T> {

  start = Math.max(0, start);
  end = Math.min(arr.length - 1, end);

  for (let i = end; i > start; i--) {
    const j = Math.floor(Math.random() * (i - start + 1)) + start;
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }

  return arr;
}

function mouseMoveHandler(ev: MouseEvent): void {
  mouseX = Math.floor((ev.pageX - leftOffset) / config.mouseScale )
  mouseY = Math.floor((ev.pageY - topOffset) / config.mouseScale)
}

function mouseDownHandler(ev: MouseEvent): void {
  if (ev.button === 0) {
    revertFlag = 1
  }
}

function mouseUpHandler(ev: MouseEvent): void {
  if (ev.button === 0) {
    revertFlag = -1
  }
}

export async function loadImages(imageSpecs: InputSpec[]): Promise<void> {
  if (imageLoaded) return
  const loadImage = (url: string): Promise<HTMLImageElement> => {
    return new Promise((resolve, reject) => { 
      const img = new Image();
      img.src = url;
      img.onload = () => resolve(img);
      img.onerror = () => reject(new Error(`Failed to load image: ${url}`));
    });
  };

  const createCanvasFromImage = (
    image: HTMLImageElement, scaleX: number, scaleY: number
  ): HTMLCanvasElement => {
    const canvas = document.createElement('canvas');
    canvas.width = image.width * scaleX;
    canvas.height = image.height * scaleY;
    const ctx = canvas.getContext('2d');
    if (ctx) {
      ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
    }
    return canvas;
  };

  const generatePoints = (
    canvas: HTMLCanvasElement,
    revert: boolean,
    alphaThreshold: number,
    brightnessThreshold: number,
    offsetX: number,
    offsetY: number
  ): PointSpec[] => {
    const points: PointSpec[] = [];
    const ctx = canvas.getContext('2d');
    if (!ctx) {
      console.error('Failed to get 2D context from canvas');
      return points;
    }
  
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;
  
    // 遍历像素数据，按步长采样
    for (let y = 0; y < canvas.height; y += config.sampleStep) {
      for (let x = 0; x < canvas.width; x += config.sampleStep) {
        const index = (y * canvas.width + x) * 4; // 每个像素占4个字节 (RGBA)
        const r = data[index];     // 红色通道
        const g = data[index + 1]; // 绿色通道
        const b = data[index + 2]; // 蓝色通道
        const a = data[index + 3]; // 透明度通道
  
        // 计算平均亮度
        let brightness = (r + g + b) / 3;
        if (a < alphaThreshold) {
          // transparent pixel
          continue
        }
        
        if (revert) {
          brightness = 255 - brightness
        }
        // 根据透明度和亮度阈值决定是否生成点
        if (brightness < brightnessThreshold) {
          const point: PointSpec = {
            originX: x - Math.floor(canvas.width / 2) + offsetX,
            originY: y - Math.floor(canvas.height / 2) + offsetY
          }
          points.push(point);
        }
      }
    }
  
    return points;
  };

  for (const spec of imageSpecs) {
    try {
      const {
        imagePath,
        revert = false,
        alphaThreshold = config.alphaThreshold,
        brightnessThreshold = config.brightnessThreshold,
        scaleX = 1.0,
        scaleY = 1.0,
        offsetX = config.offsetX,
        offsetY = config.offsetY
      } = spec;
      const img = await loadImage(`/points/${imagePath}`);
      const canvas = createCanvasFromImage(img, scaleX, scaleY);
      imageInfos.push({
        imagePoints: generatePoints(
          canvas, revert, alphaThreshold, brightnessThreshold,
          offsetX, offsetY
        ),
        height: canvas.height,
        width: canvas.width
      });
    } catch (error) {
      console.error(error);
    }
  }

  imageListSize = imageInfos.length
  imageLoaded = true
}

export function updateWindowSize() {
  leftOffset = Math.floor(window.innerWidth / 2)
  topOffset = Math.floor(window.innerHeight / 2)
}

export function adjustIndex(step: number): void {
  const old = currentIndex
  currentIndex += step
  if (currentIndex < 0) {
    currentIndex += imageListSize
  } else if (currentIndex >= imageListSize) {
    currentIndex -= imageListSize
  }
  if (old != currentIndex)
    changeImage()
}

export function stopAnimation(): void {
  for (const point of currentPoints) {
    const spec = point.randomPointSpec(config.distributeDistance)
    point.applyOrigin(spec)
    point.disappear()
  }
  window.removeEventListener("mousemove", mouseMoveHandler)
  window.removeEventListener("mousedown", mouseDownHandler)
  window.removeEventListener("mouseup", mouseUpHandler)
  revertFlag = -1
  setTimeout(() => {
    currentPoints = []
    bindCtx = null
    cancelAnimationFrame(cbNumber)
  }, config.activationDelay);
}

export function startAnimation(element: HTMLCanvasElement): void {
  setTimeout(() => {
    currentIndex = 0
    revertFlag = -1
    previousTimestamp = undefined
    window.addEventListener("mousemove", mouseMoveHandler)
    window.addEventListener("mousedown", mouseDownHandler)
    window.addEventListener("mouseup", mouseUpHandler)
    bindCtx = element.getContext("2d")
    updateWindowSize()
    changeImage()
    cbNumber = requestAnimationFrame(singleFrame)
  }, config.activationDelay);
}
