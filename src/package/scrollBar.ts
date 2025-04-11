
/**
 * Written by Darksky
 * 
 * Bar Box: hover pressed
 * Bar Inner: hover pressed
 */

const resizeDelay = 500;
const scrollFactor = 1.0;

export class VerticalScrollBar {

  sbBox: HTMLElement;
  sbInner: HTMLElement;
  scBox: HTMLElement;
  scInner: HTMLElement;

  sbBoxHeight!: number;
  sbInnerHeight!: number;
  scBoxHeight!: number;
  scInnerHeight!: number;
  originY!: number;

  boxInnerRatio!: number;
  inScrollContent: boolean;
  inScrollBar: boolean;
  mouseDown: boolean;
  trackMousePos: boolean;
  mouseY: number;
  progress: number;
  noScroll: boolean;
  clickY: number;
  dragOrigin: number;

  resizing: boolean;

  constructor (
    scrollBarBox: HTMLElement,
    scrollBarInner: HTMLElement,
    scrollContentBox: HTMLElement,
    scrollContentInner: HTMLElement
  ) {
    this.sbBox = scrollBarBox;
    this.sbInner = scrollBarInner;
    this.scBox = scrollContentBox;
    this.scInner = scrollContentInner;
    this.resizing = false;
    this.inScrollContent = false;
    this.inScrollBar = false;
    this.mouseDown = false;
    this.trackMousePos = false;
    this.mouseY = 0;
    this.progress = 0.0;
    this.noScroll = true;
    this.clickY = 0;
    this.dragOrigin = 0;
    this.updateComponentSize();
    this.updateScrollBarParams();
    this.resizeHandler = this.resizeHandler.bind(this);
    this.sbContentEnter = this.sbContentEnter.bind(this);
    this.sbContentLeave = this.sbContentLeave.bind(this);
    this.sbBarEnter = this.sbBarEnter.bind(this);
    this.sbBarLeave = this.sbBarLeave.bind(this);
    this.wheelHandler = this.wheelHandler.bind(this);
    this.sbBarMouseDown = this.sbBarMouseDown.bind(this);
    this.sbBarMouseUp = this.sbBarMouseUp.bind(this);
    this.sbMouseMove = this.sbMouseMove.bind(this);
    
    window.addEventListener("resize", this.resizeHandler);
    scrollContentBox.addEventListener("mouseenter", this.sbContentEnter);
    scrollContentBox.addEventListener("mouseleave", this.sbContentLeave);
    scrollContentBox.addEventListener("wheel", this.wheelHandler);
    scrollBarBox.addEventListener("mouseenter", this.sbBarEnter);
    scrollBarBox.addEventListener("mouseleave", this.sbBarLeave);
    scrollBarBox.addEventListener("wheel", this.wheelHandler);
    window.addEventListener("mousedown", this.sbBarMouseDown);
    window.addEventListener("mouseup", this.sbBarMouseUp);
  }

  dispose(): void {
    window.removeEventListener("resize", this.resizeHandler);
    this.scBox.removeEventListener("mouseenter", this.sbContentEnter);
    this.scBox.removeEventListener("mouseleave", this.sbContentLeave);
    this.scBox.removeEventListener("wheel", this.wheelHandler);
    this.sbBox.removeEventListener("mouseenter", this.sbBarEnter);
    this.sbBox.removeEventListener("mouseleave", this.sbBarLeave);
    this.sbBox.removeEventListener("wheel", this.wheelHandler);
    window.removeEventListener("mouseup", this.sbBarMouseUp);
    window.removeEventListener("mousedown", this.sbBarMouseDown);
    document.removeEventListener("mousemove", this.sbMouseMove);
  }

  sbContentEnter(): void {
    if (!this.noScroll) {
      this.sbBox.classList.add("semi-hover");
    }
    this.inScrollContent = true;
  }
  sbContentLeave(): void {
    this.sbBox.classList.remove("semi-hover");
    this.inScrollContent = false;
  }
  sbBarEnter(): void {
    if (!this.noScroll) {
      this.sbBox.classList.add("hover");
    }
    this.inScrollBar = true;
  }
  sbBarLeave(): void {
    this.sbBox.classList.remove("hover");
    this.inScrollBar = false;
  }
  sbBarMouseDown(event: MouseEvent): void {
    if (this.inScrollBar && !this.noScroll) {
      this.clickY = event.pageY;
      const topHeight = (this.sbBoxHeight - this.sbInnerHeight) * this.progress;
      const distance = this.clickY - this.originY - topHeight;
      if (distance > this.sbInnerHeight || distance < 0) {
        const targetTop = this.clickY - this.originY - this.sbInnerHeight / 2;
        let targetProgress = targetTop / (this.sbBoxHeight - this.sbInnerHeight);
        if (targetProgress > 0.9999) targetProgress = 1.0;
        if (targetProgress < 0.0001) targetProgress = 0.0;
        this.progress = targetProgress;
        this.updateComponentPosition();
      } else {
        this.dragOrigin = topHeight;
        this.sbBox.classList.add("pressed");
        this.scBox.classList.add("pressed");
        document.addEventListener("mousemove", this.sbMouseMove);
        this.trackMousePos = true;
      }
    }
    this.mouseDown = true;
  }
  sbBarMouseUp(): void {
    if (this.trackMousePos) {
      document.removeEventListener("mousemove", this.sbMouseMove);
    }
    this.sbBox.classList.remove("pressed");
    this.scBox.classList.remove("pressed");
    this.mouseDown = false;
    this.trackMousePos = false;
  }
  sbMouseMove(event: MouseEvent): void {
    this.mouseY = event.pageY;
    const diff = this.mouseY - this.clickY + this.dragOrigin;
    let targetProgress = diff / (this.sbBoxHeight - this.sbInnerHeight);
    if (targetProgress > 0.9999) targetProgress = 1.0;
    if (targetProgress < 0.0001) targetProgress = 0.0;
    this.progress = targetProgress;
    this.updateComponentPosition();
  }

  resizeHandler(): void {
    if (!this.resizing) {
      this.resizing = true;
      setTimeout(() => {
        this.updateComponentSize();
        this.updateScrollBarParams();
        this.resizing = false;
      }, resizeDelay);
    }
  }

  wheelHandler(event: WheelEvent): void{
    event.stopPropagation();
    if (!this.noScroll) {
      this.progress += event.deltaY / this.scBoxHeight * scrollFactor;
      this.updateComponentPosition();
    }
  }

  updateComponentSize(): void {
    this.sbBoxHeight = this.sbBox.getBoundingClientRect().height;
    this.scBoxHeight = this.scBox.getBoundingClientRect().height;
    this.scInnerHeight = this.scInner.getBoundingClientRect().height;
    this.originY = this.sbBox.getBoundingClientRect().top;
  }

  updateScrollBarParams(): void {
    this.boxInnerRatio = this.scBoxHeight / this.scInnerHeight;
    this.sbInnerHeight = this.sbBoxHeight * this.boxInnerRatio;
    if (this.boxInnerRatio > 1.0) {
      this.noScroll = true;
      this.sbBox.classList.add("inactive");
    } else {
      this.noScroll = false;
      this.sbBox.classList.remove("inactive");
    }
    this.sbInner.style.height = `${this.sbInnerHeight}px`;
  }

  updateComponentPosition(): void {
    if (this.progress < 0.0001) this.progress = 0.0;
    if (this.progress > 0.9999) this.progress = 1.0;
    let distance = (this.sbBoxHeight - this.sbInnerHeight) * this.progress;
    this.sbInner.style.translate = `0 ${Math.floor(distance)}px`;
    distance = (this.scBoxHeight - this.scInnerHeight) * this.progress;
    this.scInner.style.translate = `0 ${Math.floor(distance)}px`;
  }

}
