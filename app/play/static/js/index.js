'use strict';

import ClickableNode from './clickableNode.js';

document.addEventListener('DOMContentLoaded', () => {
    const socket = io.connect('http://' + document.domain + ':' + location.port + '/play');
    const canvas = document.querySelector('canvas');
    const ctx = canvas.getContext('2d');
    
    const canvasLeft = canvas.offsetLeft + canvas.clientLeft;
    const canvasTop = canvas.offsetTop + canvas.clientTop;
    const offset = 50;
    const radius = 7;
    const fieldSize = 11;
    
    let moveNow = false;
    const clickableNodes = getNodes(fieldSize, offset);

    socket.on('draw field', data => {
        moveNow = data.moveNow;
        drawField(ctx, fieldSize, offset, radius);
    });

    socket.on('bot move', data => {
        /* logic here */
    });
    
    canvas.addEventListener('click', event => {
        if (moveNow) {
            const x = event.pageX - canvasLeft;
            const y = event.pageY - canvasTop;

            for (const node of clickableNodes){
                if (node.hitTest(x, y)) {
                    socket.emit('player move', (node.x, node.y)); // indides in grid
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
            clickableNodes.push(new ClickableNode(i, j, offset));
        }
    }

    return clickableNodes;
}

function drawField(ctx, fieldSize, offset, radius) {
    const blueColor = '#0000FF';
    const redColor = '#FF0000';

    for (let i = 0; i < fieldSize; ++i) {
        for(let j = !(i % 2); j < fieldSize; j += 2) {
            ctx.beginPath();
            ctx.fillStyle = (i % 2) ? blueColor: redColor;
            ctx.arc(i*offset + radius, j*offset + radius, radius, 0, 2*Math.PI);
            ctx.fill();
            ctx.closePath();
        }
    }
};

function makeMove(x, y, fMove) {
    /* logic here */
}

