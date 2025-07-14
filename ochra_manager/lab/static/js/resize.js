var resizer = document.querySelector('#RESIZER');
var container = document.querySelector('#SIDEPANEL_CONTAINER');

// When the user presses down on the resizer
resizer.addEventListener('mousedown', initDrag);

function initDrag(e) {
	window.addEventListener('mousemove', startDrag);
	window.addEventListener('mouseup', stopDrag);
}

function startDrag(e) {
	// Calculate new width based on mouse position
	// panelContainer.offsetLeft is the left position of the container
	const newWidth = (container.offsetLeft + container.offsetWidth) - e.clientX;

	// Optionally, add a minimum width:
	if (newWidth > 50 && newWidth <= 1001) {
		container.style.width = newWidth + 'px';
	}
}

function stopDrag(e) {
	window.removeEventListener('mousemove', startDrag);
	window.removeEventListener('mouseup', stopDrag);
}
