{
    // Переключатель темы
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;
    if (themeToggle) {
        themeToggle.addEventListener('change', () => {
            body.classList.toggle('light-theme', themeToggle.checked);
        });
    }

    // Переключение режимов (текст/фото)
    const tabText = document.getElementById('tabText');
    const tabPhoto = document.getElementById('tabPhoto');
    const textMode = document.getElementById('textMode');
    const photoMode = document.getElementById('photoMode');

    function setMode(mode) {
        if (mode === 'text') {
            tabText.classList.add('active');
            tabPhoto.classList.remove('active');
            textMode.classList.remove('hidden');
            photoMode.classList.add('hidden');
        } else {
            tabPhoto.classList.add('active');
            tabText.classList.remove('active');
            photoMode.classList.remove('hidden');
            textMode.classList.add('hidden');
        }
    }
    if (tabText && tabPhoto) {
        tabText.addEventListener('click', () => setMode('text'));
        tabPhoto.addEventListener('click', () => setMode('photo'));
        setMode('text');
    }

    // Свич языков
    const langSwapBtn = document.getElementById('langSwapBtn');
    const langLeft = document.getElementById('langLeft');
    const langRight = document.getElementById('langRight');
    const swapIcon = document.getElementById('swapIcon');
    const leftTextarea = document.querySelector('#leftBox textarea');
    const rightTextarea = document.querySelector('#rightBox textarea');

    let swapped = false;
    let isAnimating = false;

    if (langSwapBtn) {
        langSwapBtn.addEventListener('click', () => {
            if (isAnimating) return;
            isAnimating = true;

            // Фаза 1
            langLeft.classList.add('swap-out-left');
            langRight.classList.add('swap-out-right');

            setTimeout(() => {
                // Меняем языки
                swapped = !swapped;
                langLeft.textContent  = swapped ? 'Английский' : 'Русский';
                langRight.textContent = swapped ? 'Русский' : 'Английский';

                // Меняем 
                const tmp = leftTextarea.value;
                leftTextarea.value = rightTextarea.value;
                rightTextarea.value = tmp;

                // Вращаем иконку
                swapIcon.classList.toggle('rotated', swapped);

                // Фаза 2
                langLeft.classList.remove('swap-out-left');
                langRight.classList.remove('swap-out-right');

                setTimeout(() => { isAnimating = false; }, 150);
            }, 150);
        });
    }
}