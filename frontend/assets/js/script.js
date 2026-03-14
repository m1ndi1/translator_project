document.addEventListener("DOMContentLoaded", () => {
    const API_BASE = "/api";
    const body = document.body;
    const themeToggle = document.getElementById("themeToggle");

    const tabText = document.getElementById("tabText");
    const tabPhoto = document.getElementById("tabPhoto");
    const textMode = document.getElementById("textMode");
    const photoMode = document.getElementById("photoMode");
    const textLabel = document.getElementById("textLabel");
    const photoLabel = document.getElementById("photoLabel");

    const sourceLang = document.getElementById("sourceLang");
    const targetLang = document.getElementById("targetLang");
    const swapLanguages = document.getElementById("swapLanguages");

    const sourceText = document.getElementById("sourceText");
    const translateButton = document.getElementById("translateButton");
    const resultText = document.getElementById("resultText");
    const statusMessage = document.getElementById("statusMessage");

    const imageInput = document.getElementById("imageInput");
    const dropzone = document.getElementById("dropzone");
    const dropzoneText = document.getElementById("dropzoneText");

    function setStatus(message = "") {
        if (!message) {
            statusMessage.textContent = "";
            statusMessage.classList.add("hidden");
            return;
        }

        statusMessage.textContent = message;
        statusMessage.classList.remove("hidden");
    }

    function setMode(mode) {
        if (mode === "text") {
            tabText.classList.add("active");
            tabPhoto.classList.remove("active");
            textMode.classList.remove("hidden");
            photoMode.classList.add("hidden");
            textLabel.classList.remove("hidden");
            photoLabel.classList.add("hidden");
            return;
        }

        tabPhoto.classList.add("active");
        tabText.classList.remove("active");
        photoMode.classList.remove("hidden");
        textMode.classList.add("hidden");
        textLabel.classList.add("hidden");
        photoLabel.classList.remove("hidden");
    }

    function swapLanguagesValues() {
        const currentSource = sourceLang.value;
        sourceLang.value = targetLang.value;
        targetLang.value = currentSource;
    }

    function getApiErrorMessage(data, fallback) {
        if (!data) return fallback;
        return data.message || data.detail || fallback;
    }

    async function translateTextRequest(text, sourceLanguage, targetLanguage) {
        const response = await fetch(`${API_BASE}/translate/text`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text,
                source_language: sourceLanguage,
                target_language: targetLanguage
            })
        });

        const data = await response.json().catch(() => null);

        if (!response.ok) {
            throw new Error(getApiErrorMessage(data, "Ошибка перевода"));
        }

        return data;
    }

    async function translateImageRequest(file, sourceLanguage, targetLanguage) {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("source_language", sourceLanguage);
        formData.append("target_language", targetLanguage);

        const response = await fetch(`${API_BASE}/translate/image`, {
            method: "POST",
            body: formData
        });

        const data = await response.json().catch(() => null);

        if (!response.ok) {
            throw new Error(getApiErrorMessage(data, "Ошибка обработки изображения"));
        }

        return data;
    }

    async function handleTextTranslate() {
        const text = sourceText.value.trim();

        if (!text) {
            resultText.value = "";
            setStatus("Введите текст для перевода");
            return;
        }

        if (sourceLang.value === targetLang.value) {
            resultText.value = "";
            setStatus("Исходный и целевой языки не должны совпадать");
            return;
        }

        try {
            resultText.value = "";
            setStatus("Переводим текст...");

            const data = await translateTextRequest(
                text,
                sourceLang.value,
                targetLang.value
            );

            resultText.value = data.translated_text || "";
            setStatus("Готово");
        } catch (error) {
            console.error(error);
            resultText.value = "";
            setStatus(error.message || "Ошибка перевода");
        }
    }

    async function handleImageTranslate(file) {
        if (!file) return;

        if (sourceLang.value === targetLang.value) {
            resultText.value = "";
            setStatus("Исходный и целевой языки не должны совпадать");
            return;
        }

        try {
            resultText.value = "";
            dropzoneText.textContent = `Файл: ${file.name}`;
            setStatus("Распознаем и переводим изображение...");

            const data = await translateImageRequest(
                file,
                sourceLang.value,
                targetLang.value
            );

            resultText.value = data.translated_text || "";
            setStatus("Изображение успешно обработано");
        } catch (error) {
            console.error(error);
            resultText.value = "";
            setStatus(error.message || "Ошибка обработки изображения");
        }
    }

    if (themeToggle) {
        themeToggle.addEventListener("change", () => {
            body.classList.toggle("light-theme", themeToggle.checked);
        });
    }

    tabText.addEventListener("click", () => setMode("text"));
    tabPhoto.addEventListener("click", () => setMode("photo"));
    setMode("text");

    swapLanguages.addEventListener("click", () => {
        swapLanguagesValues();
        setStatus("");
    });

    translateButton.addEventListener("click", () => {
        handleTextTranslate();
    });

    sourceText.addEventListener("keydown", (event) => {
        if (event.ctrlKey && event.key === "Enter") {
            event.preventDefault();
            handleTextTranslate();
        }
    });

    imageInput.addEventListener("change", async (event) => {
        const file = event.target.files[0];
        if (file) {
            await handleImageTranslate(file);
        }
        imageInput.value = "";
    });

    dropzone.addEventListener("click", () => {
        imageInput.click();
    });

    dropzone.addEventListener("dragover", (event) => {
        event.preventDefault();
        dropzone.classList.add("dragover");
    });

    dropzone.addEventListener("dragleave", () => {
        dropzone.classList.remove("dragover");
    });

    dropzone.addEventListener("drop", async (event) => {
        event.preventDefault();
        dropzone.classList.remove("dragover");

        const file = event.dataTransfer.files[0];
        if (file) {
            await handleImageTranslate(file);
        }
    });
});