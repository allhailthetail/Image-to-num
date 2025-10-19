const img = document.getElementById('image');
const live = document.getElementById('liveCoords');
const getBtn = document.getElementById('getCoordsBtn');
const out = document.getElementById('coordsOut');
const copyBtn = document.getElementById('copyBtn');

let cropper;

function round(n) { return Math.round(n); }

function formatCoords(data) {
    // Cropper data is in the image's natural pixel space.
    const x1 = data.x, y1 = data.y;
    const x2 = data.x + data.width;
    const y2 = data.y + data.height;
    return {
        x1: round(x1),
        y1: round(y1),
        x2: round(x2),
        y2: round(y2),
        width: round(data.width),
        height: round(data.height)
    };
}

img.addEventListener('load', () => {
    cropper = new Cropper(img, {
        // Make it a pure selection tool:
        dragMode: 'crop',            // draw/move the crop box only
        movable: false,              // image itself cannot be panned
        zoomable: false,             // disable programmatic zoom
        zoomOnWheel: false,          // disable wheel zoom
        zoomOnTouch: false,          // disable pinch zoom
        toggleDragModeOnDblclick: false,

        // Usability niceties (optional):
        viewMode: 1,
        guides: true,
        background: true,
        autoCrop: true,
        autoCropArea: 0.6,
        responsive: true,

        crop(event) {
            const d = formatCoords(event.detail);
            live.textContent =
                `x: ${d.x1}, y: ${d.y1}, x2: ${d.x2}, y2: ${d.y2}, w: ${d.width}, h: ${d.height}`;
        }
    });
});

getBtn.addEventListener('click', () => {
    if (!cropper) return;
    const data = cropper.getData(true); // true = rounded values
    const d = formatCoords(data);
    out.value = JSON.stringify(d);
});

copyBtn.addEventListener('click', async () => {
    try {
        await navigator.clipboard.writeText(out.value);
        copyBtn.textContent = 'Copied!';
        setTimeout(() => (copyBtn.textContent = 'Copy'), 900);
    } catch (_) { /* noop */ }
});
