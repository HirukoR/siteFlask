document.addEventListener('DOMContentLoaded', function() {
    // Закрытие alert-сообщений через 5 секунд
    const alerts = document.querySelectorAll('.alert');
    if (alerts) {
        alerts.forEach(function(alert) {
            setTimeout(function() {
                const closeButton = alert.querySelector('.btn-close');
                if (closeButton) {
                    closeButton.click();
                }
            }, 5000);
        });
    }
    
    // Подтверждение удаления или изменения статуса
    const confirmButtons = document.querySelectorAll('[data-confirm]');
    if (confirmButtons) {
        confirmButtons.forEach(function(button) {
            button.addEventListener('click', function(e) {
                if (!confirm(this.dataset.confirm)) {
                    e.preventDefault();
                }
            });
        });
    }
    
    // Активация текущего пункта в меню
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    if (navLinks) {
        navLinks.forEach(function(link) {
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });
    }
    
    // Обработка таблицы с возможностью сортировки
    const sortableHeaders = document.querySelectorAll('th[data-sort]');
    if (sortableHeaders) {
        sortableHeaders.forEach(function(header) {
            header.addEventListener('click', function() {
                const table = this.closest('table');
                const tbody = table.querySelector('tbody');
                const rows = Array.from(tbody.querySelectorAll('tr'));
                const index = Array.from(this.parentNode.children).indexOf(this);
                const dir = this.dataset.sort === 'asc' ? 'desc' : 'asc';
                
                // Обновление атрибута сортировки
                sortableHeaders.forEach(h => h.dataset.sort = '');
                this.dataset.sort = dir;
                
                // Сортировка строк
                rows.sort(function(a, b) {
                    const aValue = a.children[index].textContent.trim();
                    const bValue = b.children[index].textContent.trim();
                    
                    if (dir === 'asc') {
                        return aValue.localeCompare(bValue);
                    } else {
                        return bValue.localeCompare(aValue);
                    }
                });
                
                // Обновление таблицы
                rows.forEach(function(row) {
                    tbody.appendChild(row);
                });
            });
        });
    }
}); 