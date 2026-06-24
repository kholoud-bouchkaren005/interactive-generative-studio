const canvas = document.getElementById("artCanvas");

if (canvas) {
    const ctx = canvas.getContext("2d");
    const shapeType = document.getElementById("shapeType");
    const paletteSelect = document.getElementById("palette");
    const shapeSize = document.getElementById("shapeSize");
    const shapeCount = document.getElementById("shapeCount");
    const animateToggle = document.getElementById("animateToggle");
    const sizeValue = document.getElementById("sizeValue");
    const countValue = document.getElementById("countValue");
    const randomBtn = document.getElementById("randomBtn");
    const clearBtn = document.getElementById("clearBtn");
    const downloadBtn = document.getElementById("downloadBtn");

    const palettes = {
        aurora: ["#3dd6d0", "#8a5cf6", "#f7d060", "#ff7aa2"],
        citrus: ["#f25c54", "#ffb703", "#2a9d8f", "#264653"],
        mono: ["#121212", "#4b5563", "#f4f4f5", "#9ca3af"],
        neon: ["#00f5d4", "#fee440", "#f15bb5", "#00bbf9"]
    };

    const shapes = [];
    let pointerDown = false;
    let lastDragTime = 0;

    function resizeCanvas() {
        const rect = canvas.getBoundingClientRect();
        const ratio = window.devicePixelRatio || 1;
        canvas.width = Math.floor(rect.width * ratio);
        canvas.height = Math.floor(rect.height * ratio);
        ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    }

    function randomFrom(list) {
        return list[Math.floor(Math.random() * list.length)];
    }

    function getPointerPosition(event) {
        const rect = canvas.getBoundingClientRect();
        return {
            x: event.clientX - rect.left,
            y: event.clientY - rect.top
        };
    }

    function addShape(x, y) {
        const colors = palettes[paletteSelect.value];
        const baseSize = Number(shapeSize.value);
        const burst = Number(shapeCount.value);

        for (let i = 0; i < burst; i += 1) {
            shapes.push({
                x: x + (Math.random() - 0.5) * baseSize,
                y: y + (Math.random() - 0.5) * baseSize,
                size: baseSize * (0.45 + Math.random() * 0.9),
                color: randomFrom(colors),
                type: shapeType.value,
                angle: Math.random() * Math.PI * 2,
                speed: 0.003 + Math.random() * 0.012,
                drift: {
                    x: (Math.random() - 0.5) * 0.45,
                    y: (Math.random() - 0.5) * 0.45
                }
            });
        }
    }

    function drawShape(shape) {
        ctx.save();
        ctx.translate(shape.x, shape.y);
        ctx.rotate(shape.angle);
        ctx.fillStyle = shape.color;
        ctx.strokeStyle = shape.color;
        ctx.lineWidth = Math.max(2, shape.size / 12);
        ctx.globalAlpha = 0.82;

        if (shape.type === "circle") {
            ctx.beginPath();
            ctx.arc(0, 0, shape.size / 2, 0, Math.PI * 2);
            ctx.fill();
        } else if (shape.type === "square") {
            ctx.fillRect(-shape.size / 2, -shape.size / 2, shape.size, shape.size);
        } else if (shape.type === "triangle") {
            ctx.beginPath();
            ctx.moveTo(0, -shape.size / 2);
            ctx.lineTo(shape.size / 2, shape.size / 2);
            ctx.lineTo(-shape.size / 2, shape.size / 2);
            ctx.closePath();
            ctx.fill();
        } else {
            ctx.beginPath();
            ctx.moveTo(-shape.size, 0);
            ctx.lineTo(shape.size, 0);
            ctx.stroke();
        }

        ctx.restore();
    }

    function render() {
        const width = canvas.clientWidth;
        const height = canvas.clientHeight;
        ctx.clearRect(0, 0, width, height);

        const gradient = ctx.createLinearGradient(0, 0, width, height);
        gradient.addColorStop(0, "#fbfbfb");
        gradient.addColorStop(1, "#e9eef2");
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, width, height);

        shapes.forEach((shape) => {
            if (animateToggle.checked) {
                shape.angle += shape.speed;
                shape.x += shape.drift.x;
                shape.y += shape.drift.y;

                if (shape.x < -60) shape.x = width + 60;
                if (shape.x > width + 60) shape.x = -60;
                if (shape.y < -60) shape.y = height + 60;
                if (shape.y > height + 60) shape.y = -60;
            }
            drawShape(shape);
        });

        requestAnimationFrame(render);
    }

    function seedArtwork() {
        const width = canvas.clientWidth;
        const height = canvas.clientHeight;
        shapes.length = 0;
        for (let i = 0; i < 10; i += 1) {
            addShape(Math.random() * width, Math.random() * height);
        }
    }

    function syncValues() {
        sizeValue.textContent = shapeSize.value;
        countValue.textContent = shapeCount.value;
    }

    canvas.addEventListener("pointerdown", (event) => {
        pointerDown = true;
        canvas.setPointerCapture(event.pointerId);
        const point = getPointerPosition(event);
        addShape(point.x, point.y);
    });

    canvas.addEventListener("pointermove", (event) => {
        if (!pointerDown) return;
        const now = Date.now();
        if (now - lastDragTime < 55) return;
        lastDragTime = now;
        const point = getPointerPosition(event);
        addShape(point.x, point.y);
    });

    canvas.addEventListener("pointerup", () => {
        pointerDown = false;
    });

    canvas.addEventListener("pointerleave", () => {
        pointerDown = false;
    });

    shapeSize.addEventListener("input", syncValues);
    shapeCount.addEventListener("input", syncValues);
    randomBtn.addEventListener("click", seedArtwork);
    clearBtn.addEventListener("click", () => {
        shapes.length = 0;
    });
    downloadBtn.addEventListener("click", () => {
        const link = document.createElement("a");
        link.download = "interactive-artwork.png";
        link.href = canvas.toDataURL("image/png");
        link.click();
    });

    window.addEventListener("resize", () => {
        resizeCanvas();
        seedArtwork();
    });

    syncValues();
    resizeCanvas();
    seedArtwork();
    render();
}

const paletteForm = document.getElementById("paletteForm");

if (paletteForm) {
    const imageInput = document.getElementById("imageInput");
    const colorCount = document.getElementById("colorCount");
    const colorCountValue = document.getElementById("colorCountValue");
    const paletteMessage = document.getElementById("paletteMessage");
    const paletteResult = document.getElementById("paletteResult");
    const imagePreview = document.getElementById("imagePreview");

    function showPreview(file) {
        imagePreview.innerHTML = "";
        if (!file) return;

        const img = document.createElement("img");
        img.src = URL.createObjectURL(file);
        img.alt = "Uploaded artwork preview";
        img.onload = () => URL.revokeObjectURL(img.src);
        imagePreview.appendChild(img);
    }

    function renderPalette(colors) {
        paletteResult.innerHTML = "";
        colors.forEach((color) => {
            const swatch = document.createElement("article");
            swatch.className = "palette-swatch";
            swatch.innerHTML = `
                <div class="swatch-color" style="background:${color.hex}"></div>
                <div>
                    <strong>${color.hex}</strong>
                    <span>RGB ${color.rgb.join(", ")} - ${color.percentage}%</span>
                </div>
            `;
            paletteResult.appendChild(swatch);
        });
    }

    colorCount.addEventListener("input", () => {
        colorCountValue.textContent = colorCount.value;
    });

    imageInput.addEventListener("change", () => {
        showPreview(imageInput.files[0]);
    });

    paletteForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        paletteMessage.textContent = "Extracting colors...";
        paletteResult.innerHTML = "";

        const formData = new FormData(paletteForm);
        try {
            const response = await fetch("/ml-palette", {
                method: "POST",
                body: formData,
            });
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Palette extraction failed");
            }

            renderPalette(data.palette);
            paletteMessage.textContent = "Palette extracted with K-means clustering.";
        } catch (error) {
            paletteMessage.textContent = error.message;
        }
    });
}
