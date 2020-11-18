'use strict';

import ClickableNode from './clickableNode.js';
import {BLUE_COLOR, RED_COLOR, FIELD_SIZE, OFFSET, RADIOUS, LINE_WIDTH} from './const.js';

document.addEventListener('DOMContentLoaded', () => {
    const socket = io.connect('http://' + document.domain + ':' + location.port + '/play');
    const canvas = document.querySelector('canvas');
    const ctx = canvas.getContext('2d');

    let moveNow = false;
    const clickableNodes = getNodes();

    canvas.addEventListener('click', event => {
        if (moveNow) {
            const canvasLeft = canvas.offsetLeft + canvas.clientLeft;
            const canvasTop = canvas.offsetTop + canvas.clientTop;
            const x = event.pageX - canvasLeft;
            const y = event.pageY - canvasTop;

            for (const node of clickableNodes){
                if (node.hitTest(x, y)) {
                    socket.emit('validate move', {'x': node.x, 'y': node.y}); // indides in grid
                    break;
                }
            }
        }
    });

    socket.on('draw field', data => {
        moveNow = data.moveNow;
        drawField(ctx);
        if (!moveNow) { // request for bot move
            socket.emit('is over');
        }
    });

    socket.on('bot move', data => {
        makeMove(ctx, data.x, data.y, data.color);
        moveNow = true;
    });

    socket.on('player move', (data) => {
        makeMove(ctx, data.x, data.y, data.color);
        moveNow = false;
        socket.emit('is over');
    });

    socket.on('game is over', winner => {
        alert(`${(winner) ? 'Blue' : 'Red'} player won!`);
        socket.disconnect();
    });
});

function getNodes() {
    let clickableNodes = [];

    for (let i = 0; i < FIELD_SIZE; ++i) {
        for (let j = (i % 2); j < FIELD_SIZE; j += 2) {
            clickableNodes.push(new ClickableNode(i, j, OFFSET, RADIOUS));
        }
    }

    return clickableNodes;
}

function drawField(ctx) {
    for (let i = 0; i < FIELD_SIZE; ++i) {
        for(let j = !(i % 2); j < FIELD_SIZE; j += 2) {
            ctx.beginPath();
            ctx.fillStyle = (i % 2) ? BLUE_COLOR: RED_COLOR;
            ctx.arc(i*OFFSET + RADIOUS, j*OFFSET + RADIOUS, RADIOUS, 0, 2*Math.PI);
            ctx.fill();
        }
    }
};

function makeMove(ctx, y, x, fMove) {
    ctx.beginPath();
    const offsetX = (fMove && !(x & 1) || !fMove && (x & 1)) ? OFFSET : 0;
    const offsetY = (fMove && (x & 1) || !fMove && !(x & 1)) ? OFFSET : 0;
    x = x * OFFSET + RADIOUS;
    y = y * OFFSET + RADIOUS;
    ctx.strokeStyle = (fMove) ? BLUE_COLOR : RED_COLOR;
    ctx.moveTo(x - offsetX, y - offsetY);
    ctx.lineWidth = LINE_WIDTH;
    ctx.lineTo(x + offsetX, y + offsetY);
    ctx.stroke();
    ctx.closePath();
}