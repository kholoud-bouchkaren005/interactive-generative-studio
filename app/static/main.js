const canvas = document.getElementById("artCanvas");

document.documentElement.style.scrollBehavior = "smooth";

document.querySelectorAll("input[type='range']").forEach((range) => {
    const target = document.querySelector(`[data-range-value="${range.id}"]`);
    if (!target) return;

    range.addEventListener("input", () => {
        target.textContent = range.value;
    });
});

document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", () => {
        const button = form.querySelector("button[type='submit']");
        if (!button || button.classList.contains("loading")) return;
        button.dataset.originalText = button.textContent;
        button.textContent = "";
        button.classList.add("loading");
    });
});

const heroTitle = document.querySelector("[data-typing]");

if (heroTitle) {
    const text = heroTitle.dataset.typing;
    let index = 0;
    heroTitle.textContent = "";

    const typeNext = () => {
        heroTitle.textContent = text.slice(0, index);
        index += 1;
        if (index <= text.length) {
            window.setTimeout(typeNext, 54);
        }
    };

    typeNext();
}

document.querySelectorAll("[data-preview-target]").forEach((input) => {
    input.addEventListener("change", () => {
        const target = document.getElementById(input.dataset.previewTarget);
        const file = input.files[0];
        if (!target || !file) return;

        target.innerHTML = "";
        const img = document.createElement("img");
        img.src = URL.createObjectURL(file);
        img.alt = "Original image preview";
        img.onload = () => URL.revokeObjectURL(img.src);
        target.appendChild(img);
    });
});

if (canvas) {
    const ctx = canvas.getContext("2d");
    const shapeType = document.getElementById("shapeType");
    const paletteSelect = document.getElementById("palette");
    const symmetryMode = document.getElementById("symmetryMode");
    const shapeSize = document.getElementById("shapeSize");
    const shapeCount = document.getElementById("shapeCount");
    const animateToggle = document.getElementById("animateToggle");
    const gravityToggle = document.getElementById("gravityToggle");
    const sizeValue = document.getElementById("sizeValue");
    const countValue = document.getElementById("countValue");
    const randomBtn = document.getElementById("randomBtn");
    const clearBtn = document.getElementById("clearBtn");
    const downloadBtn = document.getElementById("downloadBtn");
    const brushPresetButtons = document.querySelectorAll("[data-brush-preset]");

    const palettes = {
        aurora: ["#3dd6d0", "#8a5cf6", "#f7d060", "#ff7aa2"],
        citrus: ["#f25c54", "#ffb703", "#2a9d8f", "#264653"],
        mono: ["#121212", "#4b5563", "#f4f4f5", "#9ca3af"],
        neon: ["#00f5d4", "#fee440", "#f15bb5", "#00bbf9"],
        steel: ["#4da3ff", "#ff8a3d", "#9d7bff", "#6ee7d8"],
        sunrise: ["#ff8a3d", "#ffd166", "#ef476f", "#9d7bff"],
        lagoon: ["#0eadb8", "#6ee7d8", "#4da3ff", "#e7ecf5"],
        candy: ["#ff70a6", "#ff9770", "#ffd670", "#9d7bff"]
    };

    const brushPresets = {
        soft: { shape: "circle", palette: "lagoon", size: 24, count: 3, symmetry: "off", gravity: false },
        spark: { shape: "spark", palette: "steel", size: 34, count: 6, symmetry: "mirror", gravity: false },
        bold: { shape: "star", palette: "sunrise", size: 56, count: 10, symmetry: "mandala", gravity: true }
    };

    const shapes = [];
    const strokes = [];
    let pointerDown = false;
    let lastDragTime = 0;
    let activeStroke = null;

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

    function getSymmetryPoints(point) {
        const mode = symmetryMode.value;
        const width = canvas.clientWidth;
        const height = canvas.clientHeight;

        if (mode === "mirror") {
            return [
                point,
                { x: width - point.x, y: point.y }
            ];
        }

        if (mode === "mandala") {
            const centerX = width / 2;
            const centerY = height / 2;
            const dx = point.x - centerX;
            const dy = point.y - centerY;
            const points = [];
            for (let i = 0; i < 8; i += 1) {
                const angle = (Math.PI * 2 * i) / 8;
                const cos = Math.cos(angle);
                const sin = Math.sin(angle);
                points.push({
                    x: centerX + dx * cos - dy * sin,
                    y: centerY + dx * sin + dy * cos
                });
            }
            return points;
        }

        return [point];
    }

    function addShape(x, y) {
        const colors = palettes[paletteSelect.value];
        const baseSize = Number(shapeSize.value);
        const symmetryMultiplier = symmetryMode.value === "mandala" ? 2 : 1;
        const burst = Math.max(1, Math.floor(Number(shapeCount.value) / symmetryMultiplier));

        for (let i = 0; i < burst; i += 1) {
            shapes.push({
                x: x + (Math.random() - 0.5) * baseSize,
                y: y + (Math.random() - 0.5) * baseSize,
                size: baseSize * (0.45 + Math.random() * 0.9),
                color: randomFrom(colors),
                type: shapeType.value,
                angle: Math.random() * Math.PI * 2,
                speed: 0.003 + Math.random() * 0.012,
                orbit: 0.002 + Math.random() * 0.008,
                drift: {
                    x: (Math.random() - 0.5) * 0.45,
                    y: (Math.random() - 0.5) * 0.45
                }
            });
        }
    }

    function beginStrokeAtPoint(point) {
        const points = getSymmetryPoints(point);
        activeStroke = {
            color: randomFrom(palettes[paletteSelect.value]),
            width: Math.max(3, Number(shapeSize.value) / 6),
            branches: points.map((branchPoint) => [branchPoint])
        };
        strokes.push(activeStroke);
    }

    function extendStrokeAtPoint(point) {
        if (!activeStroke) return;

        const colors = palettes[paletteSelect.value];
        const points = getSymmetryPoints(point);
        activeStroke.branches.forEach((branch, index) => {
            branch.push(points[index] || point);
        });
        if (activeStroke.branches[0].length % 5 === 0) {
            activeStroke.color = randomFrom(colors);
        }
    }

    function drawStrokeBranch(points) {
        if (points.length < 2) return;

        ctx.beginPath();
        ctx.moveTo(points[0].x, points[0].y);
        for (let i = 1; i < points.length - 1; i += 1) {
            const current = points[i];
            const next = points[i + 1];
            const midX = (current.x + next.x) / 2;
            const midY = (current.y + next.y) / 2;
            ctx.quadraticCurveTo(current.x, current.y, midX, midY);
        }

        const last = points[points.length - 1];
        ctx.lineTo(last.x, last.y);
        ctx.stroke();
    }

    function drawStroke(stroke) {
        ctx.save();
        ctx.lineCap = "round";
        ctx.lineJoin = "round";
        ctx.lineWidth = stroke.width;
        ctx.strokeStyle = stroke.color;
        ctx.shadowColor = stroke.color;
        ctx.shadowBlur = stroke.width * 2.4;
        ctx.globalAlpha = 0.72;

        if (stroke.branches) {
            stroke.branches.forEach(drawStrokeBranch);
        }

        ctx.restore();
    }

    function drawShape(shape) {
        ctx.save();
        ctx.translate(shape.x, shape.y);
        ctx.rotate(shape.angle);
        ctx.fillStyle = shape.color;
        ctx.strokeStyle = shape.color;
        ctx.lineWidth = Math.max(2, shape.size / 12);
        ctx.globalAlpha = 0.82;
        ctx.shadowColor = shape.color;
        ctx.shadowBlur = Math.max(0, shape.size / 4);

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
        } else if (shape.type === "star") {
            ctx.beginPath();
            for (let i = 0; i < 10; i += 1) {
                const radius = i % 2 === 0 ? shape.size / 2 : shape.size / 4;
                const point = (Math.PI * 2 * i) / 10 - Math.PI / 2;
                const px = Math.cos(point) * radius;
                const py = Math.sin(point) * radius;
                if (i === 0) ctx.moveTo(px, py);
                else ctx.lineTo(px, py);
            }
            ctx.closePath();
            ctx.fill();
        } else if (shape.type === "diamond") {
            ctx.beginPath();
            ctx.moveTo(0, -shape.size / 2);
            ctx.lineTo(shape.size / 2, 0);
            ctx.lineTo(0, shape.size / 2);
            ctx.lineTo(-shape.size / 2, 0);
            ctx.closePath();
            ctx.fill();
        } else if (shape.type === "ring") {
            ctx.beginPath();
            ctx.arc(0, 0, shape.size / 2, 0, Math.PI * 2);
            ctx.stroke();
            ctx.beginPath();
            ctx.arc(0, 0, shape.size / 4, 0, Math.PI * 2);
            ctx.stroke();
        } else if (shape.type === "spark") {
            ctx.beginPath();
            ctx.moveTo(-shape.size / 2, 0);
            ctx.lineTo(shape.size / 2, 0);
            ctx.moveTo(0, -shape.size / 2);
            ctx.lineTo(0, shape.size / 2);
            ctx.moveTo(-shape.size / 3, -shape.size / 3);
            ctx.lineTo(shape.size / 3, shape.size / 3);
            ctx.moveTo(shape.size / 3, -shape.size / 3);
            ctx.lineTo(-shape.size / 3, shape.size / 3);
            ctx.stroke();
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
        gradient.addColorStop(0, "#1c2535");
        gradient.addColorStop(1, "#2e3648");
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, width, height);

        ctx.save();
        ctx.strokeStyle = "rgba(231, 236, 245, 0.055)";
        ctx.lineWidth = 1;
        for (let x = 0; x < width; x += 48) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, height);
            ctx.stroke();
        }
        for (let y = 0; y < height; y += 48) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
            ctx.stroke();
        }
        ctx.restore();

        strokes.forEach(drawStroke);

        shapes.forEach((shape) => {
            if (animateToggle.checked) {
                shape.angle += shape.speed;
                if (gravityToggle.checked) {
                    const centerX = width / 2;
                    const centerY = height / 2;
                    const dx = shape.x - centerX;
                    const dy = shape.y - centerY;
                    const pull = 0.0018;
                    shape.x += -dy * shape.orbit - dx * pull;
                    shape.y += dx * shape.orbit - dy * pull;
                } else {
                    shape.x += shape.drift.x;
                    shape.y += shape.drift.y;
                }

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
        strokes.length = 0;
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
        beginStrokeAtPoint(point);
        getSymmetryPoints(point).forEach((branchPoint) => addShape(branchPoint.x, branchPoint.y));
    });

    canvas.addEventListener("pointermove", (event) => {
        if (!pointerDown) return;
        const point = getPointerPosition(event);
        extendStrokeAtPoint(point);

        const now = Date.now();
        if (now - lastDragTime < 55) return;
        lastDragTime = now;
        getSymmetryPoints(point).forEach((branchPoint) => addShape(branchPoint.x, branchPoint.y));
    });

    canvas.addEventListener("pointerup", () => {
        pointerDown = false;
        activeStroke = null;
    });

    canvas.addEventListener("pointerleave", () => {
        pointerDown = false;
        activeStroke = null;
    });

    shapeSize.addEventListener("input", syncValues);
    shapeCount.addEventListener("input", syncValues);
    brushPresetButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const preset = brushPresets[button.dataset.brushPreset];
            if (!preset) return;

            shapeType.value = preset.shape;
            paletteSelect.value = preset.palette;
            symmetryMode.value = preset.symmetry;
            gravityToggle.checked = preset.gravity;
            shapeSize.value = preset.size;
            shapeCount.value = preset.count;
            brushPresetButtons.forEach((item) => item.classList.remove("active"));
            button.classList.add("active");
            syncValues();
        });
    });
    randomBtn.addEventListener("click", seedArtwork);
    clearBtn.addEventListener("click", () => {
        shapes.length = 0;
        strokes.length = 0;
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
    const paletteResult = document.getElementById("palette-results");
    const imagePreview = document.getElementById("imagePreview");
    const imageMeta = document.getElementById("imageMeta");
    const paletteBar = document.getElementById("paletteBar");
    const presetButtons = document.querySelectorAll("[data-color-preset]");

    function formatBytes(bytes) {
        if (!bytes) return "0 KB";
        const units = ["B", "KB", "MB"];
        let size = bytes;
        let unitIndex = 0;
        while (size >= 1024 && unitIndex < units.length - 1) {
            size /= 1024;
            unitIndex += 1;
        }
        return `${size.toFixed(unitIndex === 0 ? 0 : 1)} ${units[unitIndex]}`;
    }

    function showPreview(file) {
        imagePreview.innerHTML = "";
        imagePreview.classList.remove("empty-preview");
        if (!file) {
            imagePreview.classList.add("empty-preview");
            imageMeta.textContent = "No image selected";
            return;
        }

        const img = document.createElement("img");
        img.src = URL.createObjectURL(file);
        img.alt = "Uploaded artwork preview";
        img.onload = () => URL.revokeObjectURL(img.src);
        imagePreview.appendChild(img);
        imageMeta.textContent = `${file.name} - ${formatBytes(file.size)}`;
    }

    function renderPalette(colors) {
        paletteResult.innerHTML = "";
        paletteResult.classList.remove("empty-palette");
        paletteBar.innerHTML = "";
        colors.forEach((color, index) => {
            const swatch = document.createElement("article");
            swatch.className = "palette-swatch";
            swatch.innerHTML = `
                <div class="swatch-color" style="background:${color.hex}"></div>
                <div>
                    <strong>${color.hex}</strong>
                    <span>RGB ${color.rgb.join(", ")}</span>
                    <span>${color.percentage}%</span>
                </div>
                <button type="button" class="copy-color" data-copy-color="${color.hex}">Copy</button>
            `;
            swatch.style.animationDelay = `${index * 45}ms`;
            paletteResult.appendChild(swatch);

            const segment = document.createElement("span");
            segment.style.background = color.hex;
            segment.style.width = `${color.percentage}%`;
            segment.title = `${color.hex} ${color.percentage}%`;
            paletteBar.appendChild(segment);
        });
    }

    colorCount.addEventListener("input", () => {
        colorCountValue.textContent = colorCount.value;
        presetButtons.forEach((button) => {
            button.classList.toggle("active", button.dataset.colorPreset === colorCount.value);
        });
    });

    presetButtons.forEach((button) => {
        button.addEventListener("click", () => {
            colorCount.value = button.dataset.colorPreset;
            colorCount.dispatchEvent(new Event("input"));
        });
    });

    imageInput.addEventListener("change", () => {
        showPreview(imageInput.files[0]);
    });

    paletteResult.addEventListener("click", async (event) => {
        const button = event.target.closest("[data-copy-color]");
        if (!button) return;

        const color = button.dataset.copyColor;
        try {
            await navigator.clipboard.writeText(color);
            button.textContent = "Copied";
            window.setTimeout(() => {
                button.textContent = "Copy";
            }, 1100);
        } catch (error) {
            paletteMessage.textContent = `Copy manually: ${color}`;
        }
    });

    paletteForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        paletteMessage.textContent = "Extracting colors...";
        paletteResult.innerHTML = "";
        paletteResult.classList.remove("empty-palette");
        paletteBar.innerHTML = "";

        const formData = new FormData(paletteForm);
        const button = paletteForm.querySelector("button[type='submit']");
        try {
            const response = await fetch("/extract-palette", {
                method: "POST",
                body: formData,
            });
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Palette extraction failed");
            }

            renderPalette(data.palette);
            paletteMessage.textContent = "Palette generated. Use Copy to reuse any color.";
        } catch (error) {
            paletteMessage.textContent = error.message;
            paletteResult.classList.add("empty-palette");
            paletteResult.innerHTML = `
                <article>
                    <strong>No palette yet</strong>
                    <span>${error.message}</span>
                </article>
            `;
        } finally {
            if (button) {
                button.classList.remove("loading");
                button.textContent = button.dataset.originalText || "Generate Palette";
            }
        }
    });
}
