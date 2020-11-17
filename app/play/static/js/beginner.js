'use strict';

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('input[type="radio"]').forEach(element => {
        element.addEventListener('change', () => {
            if (element.checked) {
                const beginner = document.querySelector('.beginner');
                if (element.name == 'color') {
                    beginner.style.color = (+element.value) ? '#0000FF': '#FF0000';
                } else {
                    beginner.innerHTML = (+element.value) ? 'Player' : 'Computer';
                }
            };
        })
    });
});