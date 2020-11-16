export default class ClickableNode {
    constructor(x, y, offset) {
        this.x = x;        // positions in grid
        this.y = y;
        this.topX = x * offset; // positions on canvas
        this.topY = y * offset;
        this.botX = (x + 1) * offset;
        this.botY = (y + 1) * offset;
    }

    hitTest(x, y) {
        return x > this.topX && x < this.botX &&
            y > this.topY && y < this.botY;
    }
}
