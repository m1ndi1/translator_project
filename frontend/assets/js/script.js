document.addEventListener("DOMContentLoaded", () => {
    const API_BASE = "/api";
    const THEME_STORAGE_KEY = "thebesttranslator-theme";
    const SUPPORTED_IMAGE_TYPES = new Set(["image/png", "image/jpeg"]);

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

    const defaultDropzoneText = dropzoneText.textContent;
    let isBusy = false;

    function setStatus(message = "") {
        statusMessage.textContent = message;
        statusMessage.classList.toggle("hidden", !message);
    }

    function clearResult() {
        resultText.value = "";
    }

    function setBusy(busy) {
        isBusy = busy;
        translateButton.disabled = busy;
        imageInput.disabled = busy;
        dropzone.classList.toggle("is-disabled", busy);
        body.classList.toggle("is-busy", busy);
    }

    function setMode(mode) {
        const isTextMode = mode === "text";
        tabText.classList.toggle("active", isTextMode);
        tabPhoto.classList.toggle("active", !isTextMode);
        textMode.classList.toggle("hidden", !isTextMode);
        photoMode.classList.toggle("hidden", isTextMode);
        textLabel.classList.toggle("hidden", !isTextMode);
        photoLabel.classList.toggle("hidden", isTextMode);
        setStatus("");
    }

    function setTheme(isLightTheme) {
        body.classList.toggle("light-theme", isLightTheme);
        themeToggle.checked = isLightTheme;
        localStorage.setItem(THEME_STORAGE_KEY, isLightTheme ? "light" : "dark");
    }

    function initializeTheme() {
        const savedTheme = localStorage.getItem(THEME_STORAGE_KEY);
        if (savedTheme) {
            setTheme(savedTheme === "light");
        }
    }

    function swapLanguageValues() {
        const currentSource = sourceLang.value;
        sourceLang.value = targetLang.value;
        targetLang.value = currentSource;
    }

    function getApiErrorMessage(data, fallback) {
        if (!data) {
            return fallback;
        }

        if (typeof data.detail === "string") {
            return data.detail;
        }

        if (Array.isArray(data.detail)) {
            return data.detail
                .map((item) => item.msg || item.message || "Некорректные данные")
                .join("; ");
        }

        if (typeof data.message === "string") {
            return data.message;
        }

        return fallback;
    }

    async function parseResponseJson(response) {
        return response.json().catch(() => null);
    }

    async function translateTextRequest(text, sourceLanguage, targetLanguage) {
        const response = await fetch(`${API_BASE}/translate/text`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text,
                source_language: sourceLanguage,
                target_language: targetLanguage
            })
        });

        const data = await parseResponseJson(response);
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

        const data = await parseResponseJson(response);
        if (!response.ok) {
            throw new Error(getApiErrorMessage(data, "Ошибка обработки изображения"));
        }

        return data;
    }

    function validateLanguageSelection() {
        if (sourceLang.value === targetLang.value) {
            clearResult();
            setStatus("Исходный и целевой языки не должны совпадать");
            return false;
        }

        return true;
    }

    function validateSelectedImage(file) {
        if (!file) {
            return false;
        }

        if (!SUPPORTED_IMAGE_TYPES.has(file.type)) {
            clearResult();
            setStatus("Допустимы только изображения PNG и JPEG");
            return false;
        }

        return true;
    }

    async function handleTextTranslate() {
        if (isBusy) {
            return;
        }

        const text = sourceText.value.trim();
        if (!text) {
            clearResult();
            setStatus("Введите текст для перевода");
            return;
        }

        if (!validateLanguageSelection()) {
            return;
        }

        try {
            setBusy(true);
            clearResult();
            setStatus("Переводим текст...");

            const data = await translateTextRequest(text, sourceLang.value, targetLang.value);
            resultText.value = data.translated_text || "";
            setStatus("Готово");
        } catch (error) {
            console.error(error);
            clearResult();
            setStatus(error.message || "Ошибка перевода");
        } finally {
            setBusy(false);
        }
    }

    async function handleImageTranslate(file) {
        if (isBusy || !validateSelectedImage(file)) {
            return;
        }

        if (!validateLanguageSelection()) {
            return;
        }

        try {
            setBusy(true);
            clearResult();
            dropzoneText.textContent = `Файл: ${file.name}`;
            setStatus("Распознаем и переводим изображение...");

            const data = await translateImageRequest(file, sourceLang.value, targetLang.value);
            resultText.value = data.translated_text || "";
            setStatus("Изображение успешно обработано");
        } catch (error) {
            console.error(error);
            clearResult();
            setStatus(error.message || "Ошибка обработки изображения");
        } finally {
            setBusy(false);
        }
    }

    initializeTheme();

    if (themeToggle) {
        themeToggle.addEventListener("change", () => {
            setTheme(themeToggle.checked);
        });
    }

    tabText.addEventListener("click", () => setMode("text"));
    tabPhoto.addEventListener("click", () => setMode("photo"));
    setMode("text");

    swapLanguages.addEventListener("click", () => {
        if (isBusy) {
            return;
        }

        swapLanguageValues();
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
        if (!isBusy) {
            imageInput.click();
        }
    });

    dropzone.addEventListener("dragover", (event) => {
        if (isBusy) {
            return;
        }

        event.preventDefault();
        dropzone.classList.add("dragover");
    });

    dropzone.addEventListener("dragleave", () => {
        dropzone.classList.remove("dragover");
    });

    dropzone.addEventListener("drop", async (event) => {
        event.preventDefault();
        dropzone.classList.remove("dragover");

        if (isBusy) {
            return;
        }

        const file = event.dataTransfer.files[0];
        if (file) {
            await handleImageTranslate(file);
        }
    });

    window.addEventListener("focus", () => {
        if (!isBusy && !imageInput.value) {
            dropzoneText.textContent = defaultDropzoneText;
        }
    });
});
