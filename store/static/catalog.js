document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.querySelector('.catalog-button');
    const drawer = document.querySelector('#catalog-drawer');

    if (!toggle || !drawer) {
        initializeCarousels();
        return;
    }

    const closeButton = drawer.querySelector('.catalog-drawer-close');
    const backdrop = drawer.querySelector('.catalog-drawer-backdrop');
    let closeTimer;
    let openFrame;

    const updateDrawerPosition = () => {
        const header = document.querySelector('.main-header');
        if (header) {
            drawer.style.setProperty('--catalog-drawer-top', `${header.getBoundingClientRect().bottom}px`);
        }
    };

    const closeDrawer = () => {
        if (drawer.hidden) {
            return;
        }

        window.cancelAnimationFrame(openFrame);
        drawer.classList.remove('is-open');
        document.body.classList.remove('catalog-drawer-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
        window.clearTimeout(closeTimer);
        closeTimer = window.setTimeout(() => {
            if (!drawer.classList.contains('is-open')) {
                drawer.hidden = true;
            }
        }, 280);
    };

    toggle.addEventListener('click', () => {
        if (drawer.classList.contains('is-open')) {
            closeDrawer();
            return;
        }
        window.clearTimeout(closeTimer);
        updateDrawerPosition();
        drawer.hidden = false;
        document.body.classList.add('catalog-drawer-open');
        toggle.setAttribute('aria-expanded', 'true');
        openFrame = window.requestAnimationFrame(() => drawer.classList.add('is-open'));
        closeButton.focus();
    });

    document.querySelectorAll('[data-open-catalog]').forEach((button) => {
        button.addEventListener('click', () => toggle.click());
    });

    closeButton.addEventListener('click', closeDrawer);
    backdrop.addEventListener('click', closeDrawer);

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && !drawer.hidden) {
            closeDrawer();
        }
    });

    window.addEventListener('resize', () => {
        if (!drawer.hidden) {
            updateDrawerPosition();
        }
    });

    initializeCarousels();
});

function initializeCarousels() {
    document.querySelectorAll('.carousel-track').forEach((track) => {
        const id = track.id;
        const previousButton = document.querySelector(`[data-carousel-prev="${id}"]`);
        const nextButton = document.querySelector(`[data-carousel-next="${id}"]`);
        if (!previousButton || !nextButton) {
            return;
        }

        const updateControls = () => {
            const maxScroll = track.scrollWidth - track.clientWidth;
            previousButton.disabled = track.scrollLeft <= 1;
            nextButton.disabled = maxScroll <= 1 || track.scrollLeft >= maxScroll - 1;
        };

        previousButton.addEventListener('click', () => {
            track.scrollBy({ left: -track.clientWidth * 0.8, behavior: 'smooth' });
        });
        nextButton.addEventListener('click', () => {
            track.scrollBy({ left: track.clientWidth * 0.8, behavior: 'smooth' });
        });

        track.addEventListener('scroll', updateControls, { passive: true });
        window.addEventListener('resize', updateControls);
        updateControls();
    });

    const allProductsButton = document.querySelector('.all-products-button');
    const productsTrack = document.querySelector('#products-carousel');
    if (allProductsButton && productsTrack) {
        const controls = document.querySelector('[aria-label="Перегортання товарів"]');
        allProductsButton.addEventListener('click', () => {
            const expanded = productsTrack.classList.toggle('is-expanded');
            allProductsButton.setAttribute('aria-expanded', String(expanded));
            allProductsButton.textContent = expanded ? 'Показати стрічкою ↗' : 'Усі товари ↗';
            if (controls) {
                controls.hidden = expanded;
            }
            productsTrack.scrollTo({ left: 0, behavior: 'smooth' });
            productsTrack.dispatchEvent(new Event('scroll'));
        });
    }
}
