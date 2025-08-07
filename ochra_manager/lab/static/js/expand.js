var container = document.querySelector('#SIDEPANEL_CONTAINER');
var toggleButton = document.querySelector('#TOGGLE_BUTTON');
// When the user clicks the toggle button
function toggleSidePanel() {
    const isCollapsed = container.style.width === '2rem';

    if (isCollapsed) {
        container.style.width = '30rem';  // Expanded 30rem
        toggleButton.textContent = '◀';
    } else {
        container.style.width = '2rem';  // Collapsed
        toggleButton.textContent = '▶';
    }
}

// Set initial state
container.style.width = '2rem';
toggleButton.textContent = '▶';

toggleButton.addEventListener('click', toggleSidePanel);


document.body.addEventListener('htmx:afterSwap', function (e) {
    container.style.width = '30rem';  // or whatever your expanded width is
    toggleButton.textContent = '◀';
});