'use strict';

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('input[type="radio"]').forEach(element => {
        element.addEventListener('change', () => {
            if (element.checked) {
                const beginner = document.querySelector('.beginner');
                if (element.name == 'color') {
                    beginner.style.color = (+element.value) ? '#0000FF': '#FF0000';
                } else {
                    beginner.innerHTML = (+element.value) ? 'Player' : 'Bot';
                }
            };
        })
    });
    drawButtons();
});

function drawButtons() {
    const options = document.querySelectorAll('.level button');
    const colors = ["#228B22", "#ffd500", "red"];

    for (let i = 0; i < options.length; ++i) {    
        let option = options[i];    
        let color = colors[i];

        option.style.border = `2px solid ${color}`;
        option.onmouseover = (event) => {
            event.target.style.backgroundColor = color;
        };
        option.onmouseout = (event) => {
            event.target.style.backgroundColor = "";
        };
    }
}