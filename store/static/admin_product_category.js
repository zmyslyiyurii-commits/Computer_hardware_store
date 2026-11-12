document.addEventListener('DOMContentLoaded', function () {
    if (!window.location.pathname.endsWith('/add/')) {
        return;
    }

    const categoryField = document.getElementById('id_category');
    if (!categoryField) {
        return;
    }

    categoryField.addEventListener('change', function () {
        const url = new URL(window.location.href);
        if (categoryField.value) {
            url.searchParams.set('category', categoryField.value);
        } else {
            url.searchParams.delete('category');
        }
        window.location.assign(url.toString());
    });
});
