export default class ClickableNode {
    constructor(x, y,  canvasOffset, centerOffset) {
        this.x = y;    // positions in grid
        this.y = x;
        this.radious = canvasOffset / 2;
        this.centerX = x * canvasOffset + centerOffset;
        this.centerY = y * canvasOffset + centerOffset;
    }

    hitTest(x, y) {
        return (x - this.centerX)**2 + (y - this.centerY)**2 < this.radious**2;
    }
}
