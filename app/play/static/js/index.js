'use strict';

import clickableNode from './clickableNode.js';

document.addEventListener('DOMContentLoaded', function () {
    const socket = io.connect('http://' + document.domain + ':' + location.port);
    console.log('connected');
    const canvas = document.querySelector('canvas');
    const ctx = canvas.getContext('2d');
    const offset = 500;
    let clickableNodes = getNodes();
    let fMove = true; // player moves first (for now only)

    document.querySelectorAll('.menu button').forEach(item => {
        item.addEventListener('click', event => {
            console.log('clicked');
            socket.emit('new game');
        })
    });

    socket.on('connect', function () {
        console.log('connect');
    });

    canvas.addEventListener('click', event => {
        console.log('canvas click');
        return 1;
    });

    socket.on('draw field', fieldSize => {
        console.log('draw field');
        clickableNodes = getNodes(fieldSize, offset);
        drawField(ctx, fieldSize, offset);
    });

    /*
    socket.on('valid move', move => {
        makeMove(move, fMove);
    });

    socket.on('bot move', move => {
        makeMove(move, !fMove);
    });*/
});

function getNodes(fieldSize, offset) {
    let clickableNodes = [];

    for (let i = 0; i < fieldSize; ++i) {
        for (let j = (i % 2); j < fieldSize; j += 2) {
            clickableNodes.push(clickableNode(i * offset, 2 * j * offset, offset));
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

