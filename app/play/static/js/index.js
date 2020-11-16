'use strict';

import ClickableNode from './clickableNode.js';

document.addEventListener('DOMContentLoaded', () => {
    const socket = io.connect('http://' + document.domain + ':' + location.port + '/play');
    const canvas = document.querySelector('canvas');
    const ctx = canvas.getContext('2d');
    
    const canvasLeft = canvas.offsetLeft + canvas.clientLeft;
    const canvasTop = canvas.offsetTop + canvas.clientTop;
    const offset = 50;
    const fieldSize = 11;
    
    let moveNow = false;
    const clickableNodes = getNodes(fieldSize, offset);

    socket.on('draw field', (data) => {
        moveNow = data.moveNow;
        drawField(ctx, fieldSize, offset);
    });
    
    canvas.addEventListener('click', event => {
        if (moveNow) {
            const x = event.pageX - canvasLeft;
            const y = event.pageY - canvasTop;

            for (const node of clickableNodes){
                if (node.hitTest(x, y, offset)) {
                    socket.emit('player move', (node.topX, node.topY));
                    socket.on('valid move', () => {
                        makeMove(node.topX, node.topY, moveNow);
                        moveNow != moveNow;
                    });
                }
            }
        }
    });

    
});

function getNodes(fieldSize, offset) {
    let clickableNodes = [];

    for (let i = 0; i < fieldSize; ++i) {
        for (let j = (i % 2); j < fieldSize; j += 2) {
            clickableNodes.push(new ClickableNode(i * offset, 2 * j * offset, offset));
        }
    }

    return clickableNodes;
}

function drawField(ctx, fieldSize, offset) {
    ctx.beginPath();

    for (let i = 0; i < fieldSize; ++i) {
        for(let j = !(i % 2); j < fieldSize; j += 2) {
            ctx.fillStyle = '#123456';
            ctx.arc(offset/2, offset/2, offset/2, 0, 2*Math.PI);
            ctx.fill();
        }
    }

    ctx.closePath();
};

