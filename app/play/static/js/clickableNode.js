export default class ClickableNode {
    constructor(x, y,  canvasOffset, centerOffset) {
        this.x = x;    // positions in grid
        this.y = y;
        this.radious = canvasOffset / 2;
        this.centerX = x * canvasOffset + centerOffset;
        this.centerY = y * canvasOffset + centerOffset;
    }

    hitTest(x, y) {
        return (x - this.centerY)**2 + (y - this.centerX)**2 < this.radious**2;
    }
}
