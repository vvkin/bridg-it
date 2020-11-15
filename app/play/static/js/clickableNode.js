class ClickableNode {
    constructor(topX, topY, size) {
        this.topX = topX;
        this.topY = topY;
        this.botX = topX + size;
        this.botY = topY + size;
    }

    hitTest(x, y, area) {
        return x > (topX * area) && x < (botX * area) &&
            y > (topY * area) && y < (botX * area);
    }
}
