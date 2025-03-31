// Основной JS-файл для кафе-менеджмента

document.addEventListener('DOMContentLoaded', function() {
    // Инициализация всех компонентов
    initTooltips();
    initDashboardCards();
    initDataTables();
    initOrderCards();
    initAnimations();
    initNotifications();
    initFilterToggle();
    
    // Инициализация чарта статистики, если он существует
    const statsCanvas = document.getElementById('ordersStatsChart');
    if (statsCanvas) {
        initOrdersChart(statsCanvas);
    }
    
    // Дополнительные эффекты для неонового черно-фиолетового дизайна
    initNeonNavEffects();
    initDarkModals();
    initNeonAvatars();
    initCardEffects();
    initTableEffects();
    checkNotifications();
    
    // Эффекты для форм
    const inputs = document.querySelectorAll('.form-control, .form-select');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.boxShadow = '0 0 0 0.25rem rgba(142, 36, 170, 0.25)';
            this.style.borderColor = 'var(--primary-color)';
        });
        
        input.addEventListener('blur', function() {
            this.style.boxShadow = '';
            this.style.borderColor = '';
        });
    });
    
    // Добавляем класс для темной темы к формам
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const formControls = form.querySelectorAll('.form-control, .form-select');
        formControls.forEach(control => {
            control.classList.add('dark-input');
        });
    });
    
    // Добавление неоновых стилей для кнопок
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            if (this.classList.contains('btn-primary')) {
                this.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.4), var(--neon-glow)';
            } else if (this.classList.contains('btn-success')) {
                this.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.4), 0 0 10px rgba(0, 200, 83, 0.5)';
            } else if (this.classList.contains('btn-warning')) {
                this.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.4), 0 0 10px rgba(255, 171, 0, 0.5)';
            } else if (this.classList.contains('btn-danger')) {
                this.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.4), 0 0 10px rgba(245, 0, 87, 0.5)';
            }
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.boxShadow = '';
        });
    });
    
    // Добавляем класс для стилизации темных выпадающих меню
    const style = document.createElement('style');
    style.textContent = `
        .dark-theme .dropdown-menu {
            background-color: var(--card-bg);
            border: 1px solid rgba(142, 36, 170, 0.2);
            box-shadow: var(--card-shadow);
        }
        
        .dark-theme .dropdown-item {
            color: var(--text-secondary);
        }
        
        .dark-theme .dropdown-item:hover {
            background-color: rgba(142, 36, 170, 0.1);
            color: var(--primary-color);
        }
        
        .dark-theme .dropdown-divider {
            border-top: 1px solid rgba(142, 36, 170, 0.1);
        }
        
        .neon-pulse {
            animation: neonPulse 2s infinite;
        }
        
        .neon-border {
            border-left: 4px solid var(--primary-color);
            transition: all 0.3s ease;
        }
        
        .fade-out {
            opacity: 0;
            transition: opacity 0.5s ease;
        }
        
        .card-title-glow {
            color: var(--primary-color);
            text-shadow: 0 0 5px rgba(142, 36, 170, 0.3);
        }
        
        .dark-input {
            background-color: var(--darker-color);
            color: var(--text-color);
            border: 1px solid rgba(142, 36, 170, 0.2);
        }
        
        .dark-input:focus {
            background-color: var(--darker-color);
            color: var(--text-color);
            border-color: var(--primary-color);
        }
        
        .dark-styled {
            transition: all 0.3s ease;
        }
    `;
    document.head.appendChild(style);
    
    // Добавление кнопки возврата наверх
    const backToTopButton = document.createElement('div');
    backToTopButton.className = 'back-to-top';
    backToTopButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
    document.body.appendChild(backToTopButton);
    
    // Функционал кнопки
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.classList.add('visible');
        } else {
            backToTopButton.classList.remove('visible');
        }
    });
    
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Добавление класса active-glow для активных пунктов навигации
    const activeNavLinks = document.querySelectorAll('.nav-link.active');
    activeNavLinks.forEach(link => {
        link.classList.add('active-glow');
    });
    
    // Добавление класса page-transition для основного контента
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.classList.add('page-transition');
    }
    
    // Добавление класса chart-dark для канвасов с графиками
    const chartCanvases = document.querySelectorAll('canvas.chart-canvas');
    chartCanvases.forEach(canvas => {
        canvas.classList.add('chart-dark');
    });
    
    // Применение стиля card-glass к выбранным карточкам
    const dashboardStats = document.querySelectorAll('.dashboard-stats .card');
    dashboardStats.forEach(card => {
        card.classList.add('card-glass');
    });
    
    // Обработка изображений для карточек меню
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        const img = item.querySelector('img');
        if (img) {
            const card = document.createElement('div');
            card.className = 'menu-item-card mb-4';
            
            const imgWrapper = document.createElement('div');
            imgWrapper.className = 'overflow-hidden';
            
            img.className = 'menu-item-img w-100';
            imgWrapper.appendChild(img.cloneNode(true));
            
            const cardBody = document.createElement('div');
            cardBody.className = 'card-body';
            
            const title = item.querySelector('h5, h4');
            const price = item.querySelector('.price');
            const description = item.querySelector('p:not(.price)');
            
            if (price) {
                const priceTag = document.createElement('div');
                priceTag.className = 'menu-item-price';
                priceTag.textContent = price.textContent;
                imgWrapper.appendChild(priceTag);
                price.remove();
            }
            
            if (title) {
                const titleEl = document.createElement('h5');
                titleEl.className = 'card-title neon-text mb-2';
                titleEl.textContent = title.textContent;
                cardBody.appendChild(titleEl);
                title.remove();
            }
            
            if (description) {
                const descEl = document.createElement('p');
                descEl.className = 'card-text';
                descEl.textContent = description.textContent;
                cardBody.appendChild(descEl);
                description.remove();
            }
            
            const addButton = document.createElement('button');
            addButton.className = 'btn btn-neon mt-3 w-100';
            addButton.textContent = 'Добавить в заказ';
            cardBody.appendChild(addButton);
            
            card.appendChild(imgWrapper);
            card.appendChild(cardBody);
            
            item.innerHTML = '';
            item.appendChild(card);
            item.classList.add('animated-border');
        }
    });
    
    // Замена стандартных чекбоксов на кастомные
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        if (!checkbox.closest('.custom-checkbox')) {
            const label = checkbox.closest('label') || document.createElement('label');
            if (!checkbox.closest('label')) {
                // Если чекбокс не внутри label, оборачиваем его
                const parent = checkbox.parentNode;
                label.className = 'custom-checkbox';
                
                // Если у чекбокса есть id и существует label с for="этот id"
                const linkedLabel = checkbox.id ? document.querySelector(`label[for="${checkbox.id}"]`) : null;
                if (linkedLabel) {
                    label.textContent = linkedLabel.textContent;
                    linkedLabel.remove();
                }
                
                parent.insertBefore(label, checkbox);
                label.appendChild(checkbox);
            } else {
                label.className += ' custom-checkbox';
            }
            
            const checkmark = document.createElement('span');
            checkmark.className = 'checkmark';
            label.appendChild(checkmark);
        }
    });
});

// Инициализация тултипов
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            delay: { show: 50, hide: 100 },
            animation: true
        });
    });
}

// Анимация карточек на дашборде
function initDashboardCards() {
    const cards = document.querySelectorAll('.dashboard-card');
    
    cards.forEach((card, index) => {
        // Добавляем задержку для каждой карточки, чтобы они появлялись последовательно
        setTimeout(() => {
            card.classList.add('fade-in');
        }, index * 100);
        
        // Добавляем эффект при наведении
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
            this.style.boxShadow = '0 15px 30px rgba(0, 0, 0, 0.1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.boxShadow = '';
        });
    });
}

// Инициализация DataTables для улучшенных таблиц
function initDataTables() {
    const tables = document.querySelectorAll('.data-table');
    
    tables.forEach(table => {
        $(table).DataTable({
            responsive: true,
            language: {
                search: "Поиск:",
                lengthMenu: "Показать _MENU_ записей",
                info: "Показано с _START_ по _END_ из _TOTAL_ записей",
                infoEmpty: "Показано с 0 по 0 из 0 записей",
                infoFiltered: "(отфильтровано из _MAX_ записей)",
                paginate: {
                    first: "Первая",
                    last: "Последняя",
                    next: "Следующая",
                    previous: "Предыдущая"
                }
            },
            initComplete: function() {
                // Анимация появления таблицы
                $(table).closest('.card').addClass('fade-in');
            }
        });
    });
}

// Инициализация карточек заказов
function initOrderCards() {
    const orderCards = document.querySelectorAll('.order-card');
    
    orderCards.forEach(card => {
        // Обновление прогресс-бара в реальном времени
        const progressBar = card.querySelector('.progress-bar');
        const statusBadge = card.querySelector('.status-badge');
        
        if (progressBar && statusBadge) {
            const currentValue = parseInt(progressBar.style.width, 10);
            
            // Анимация заполнения прогресс-бара
            let startValue = 0;
            const interval = setInterval(() => {
                if (startValue >= currentValue) {
                    clearInterval(interval);
                } else {
                    startValue += 1;
                    progressBar.style.width = startValue + '%';
                }
            }, 20);
        }
    });
}

// Инициализация графика заказов
function initOrdersChart(canvas) {
    // Получаем данные для графика из data-атрибута
    const chartData = JSON.parse(canvas.getAttribute('data-chart') || '{}');
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels || ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
            datasets: [{
                label: 'Заказы',
                data: chartData.data || [12, 19, 3, 5, 2, 3, 9],
                fill: true,
                backgroundColor: 'rgba(67, 97, 238, 0.2)',
                borderColor: '#4361ee',
                tension: 0.4,
                pointBackgroundColor: '#3f37c9',
                pointBorderColor: '#fff',
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.7)',
                    padding: 10,
                    bodyFont: {
                        size: 14
                    },
                    titleFont: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(200, 200, 200, 0.2)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            },
            animation: {
                duration: 2000,
                easing: 'easeOutQuart'
            }
        }
    });
}

// Инициализация анимаций
function initAnimations() {
    // Анимация всех элементов с классом .fade-in
    const fadeElements = document.querySelectorAll('.fade-in');
    
    fadeElements.forEach((element, index) => {
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 150);
    });
    
    // Добавляем анимации для таблиц
    const tables = document.querySelectorAll('.table');
    tables.forEach(table => {
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach((row, index) => {
            row.style.opacity = '0';
            row.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                row.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                row.style.opacity = '1';
                row.style.transform = 'translateY(0)';
            }, 100 + (index * 50));
        });
    });
}

// Инициализация уведомлений
function initNotifications() {
    // Находим сообщения и добавляем анимацию
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach((alert, index) => {
        // Начально скрываем
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-20px)';
        
        // Показываем с задержкой
        setTimeout(() => {
            alert.style.transition = 'all 0.5s ease';
            alert.style.opacity = '1';
            alert.style.transform = 'translateY(0)';
        }, 200 + (index * 100));
        
        // Добавляем кнопку закрытия, если её нет
        if (!alert.querySelector('.btn-close')) {
            const closeBtn = document.createElement('button');
            closeBtn.type = 'button';
            closeBtn.className = 'btn-close';
            closeBtn.setAttribute('data-bs-dismiss', 'alert');
            closeBtn.setAttribute('aria-label', 'Close');
            
            alert.appendChild(closeBtn);
            
            // Автоматически скрываем через 5 секунд
            setTimeout(() => {
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-20px)';
                
                setTimeout(() => {
                    alert.remove();
                }, 500);
            }, 5000);
        }
    });
}

// Переключение панели фильтров
function initFilterToggle() {
    const filterToggleBtn = document.querySelector('.filter-toggle-btn');
    const filterCard = document.querySelector('.filter-card');
    
    if (filterToggleBtn && filterCard) {
        filterToggleBtn.addEventListener('click', function() {
            filterCard.classList.toggle('d-none');
            
            // Обновляем иконку и текст кнопки
            const icon = this.querySelector('i');
            if (icon.classList.contains('bi-filter')) {
                icon.classList.remove('bi-filter');
                icon.classList.add('bi-x-lg');
                this.querySelector('span').textContent = 'Скрыть фильтры';
            } else {
                icon.classList.remove('bi-x-lg');
                icon.classList.add('bi-filter');
                this.querySelector('span').textContent = 'Показать фильтры';
            }
        });
    }
}

// Функция для изменения статуса заказа
function updateOrderStatus(orderId, newStatus) {
    fetch(`/api/orders/${orderId}/status`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({ status: newStatus })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Обновляем статус на странице
            const statusBadge = document.querySelector(`#order-${orderId} .status-badge`);
            if (statusBadge) {
                statusBadge.className = `badge status-badge bg-${getStatusColor(newStatus)}`;
                statusBadge.textContent = getStatusText(newStatus);
            }
            
            // Показываем уведомление
            showNotification(`Статус заказа #${orderId} изменен на "${getStatusText(newStatus)}"`, 'success');
        } else {
            showNotification('Произошла ошибка при обновлении статуса заказа', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Произошла ошибка при отправке запроса', 'danger');
    });
}

// Получение CSRF токена
function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

// Получение цвета для статуса
function getStatusColor(status) {
    const statusColors = {
        'new': 'primary',
        'in_progress': 'warning',
        'completed': 'success',
        'cancelled': 'danger'
    };
    
    return statusColors[status] || 'secondary';
}

// Получение текста для статуса
function getStatusText(status) {
    const statusTexts = {
        'new': 'Новый',
        'in_progress': 'В процессе',
        'completed': 'Выполнен',
        'cancelled': 'Отменен'
    };
    
    return statusTexts[status] || status;
}

// Показ уведомления
function showNotification(message, type = 'info') {
    const notificationsContainer = document.getElementById('notifications-container');
    
    if (!notificationsContainer) {
        // Создаем контейнер для уведомлений
        const container = document.createElement('div');
        container.id = 'notifications-container';
        container.className = 'position-fixed top-0 end-0 p-3';
        container.style.zIndex = '1050';
        document.body.appendChild(container);
    }
    
    // Создаем уведомление
    const notification = document.createElement('div');
    notification.className = `toast align-items-center text-white bg-${type} border-0`;
    notification.setAttribute('role', 'alert');
    notification.setAttribute('aria-live', 'assertive');
    notification.setAttribute('aria-atomic', 'true');
    
    notification.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    // Добавляем в контейнер
    document.getElementById('notifications-container').appendChild(notification);
    
    // Показываем
    const toast = new bootstrap.Toast(notification, { delay: 5000 });
    toast.show();
    
    // Удаляем после скрытия
    notification.addEventListener('hidden.bs.toast', function() {
        notification.remove();
    });
}

// Инициализация эффектов для навигационных элементов
function initNeonNavEffects() {
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.textShadow = 'var(--neon-glow)';
        });
        
        link.addEventListener('mouseleave', function() {
            if (!this.classList.contains('active')) {
                this.style.textShadow = 'none';
            }
        });
    });
    
    // Эффект пульсации для логотипа
    const navBrand = document.querySelector('.navbar-brand');
    if (navBrand) {
        navBrand.classList.add('neon-pulse');
    }
}

// Инициализация эффектов для модальных окон
function initDarkModals() {
    const modalTriggers = document.querySelectorAll('[data-bs-toggle="modal"]');
    
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', function() {
            setTimeout(() => {
                const modals = document.querySelectorAll('.modal-content');
                modals.forEach(modal => {
                    if (!modal.classList.contains('dark-styled')) {
                        modal.classList.add('dark-styled');
                        modal.style.backgroundColor = 'var(--card-bg)';
                        modal.style.color = 'var(--text-color)';
                        modal.style.borderLeft = '2px solid var(--primary-color)';
                        modal.style.boxShadow = 'var(--card-shadow), var(--neon-glow)';
                        
                        const modalHeader = modal.querySelector('.modal-header');
                        if (modalHeader) {
                            modalHeader.style.borderBottom = '1px solid rgba(142, 36, 170, 0.2)';
                        }
                        
                        const modalFooter = modal.querySelector('.modal-footer');
                        if (modalFooter) {
                            modalFooter.style.borderTop = '1px solid rgba(142, 36, 170, 0.2)';
                        }
                    }
                });
            }, 50);
        });
    });
}

// Неоновые эффекты для аватаров
function initNeonAvatars() {
    const avatars = document.querySelectorAll('.avatar');
    
    avatars.forEach(avatar => {
        avatar.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 0 15px rgba(142, 36, 170, 0.8), 0 0 30px rgba(142, 36, 170, 0.5)';
            this.style.transform = 'scale(1.1)';
        });
        
        avatar.addEventListener('mouseleave', function() {
            this.style.boxShadow = 'var(--neon-glow)';
            this.style.transform = 'scale(1)';
        });
    });
}

// Инициализация эффектов для карточек
function initCardEffects() {
    const cards = document.querySelectorAll('.card:not(.dashboard-card)');
    
    cards.forEach(card => {
        // Добавляем неоновый бордер при наведении
        card.addEventListener('mouseenter', function() {
            this.style.boxShadow = 'var(--card-shadow-hover), var(--neon-glow)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.boxShadow = 'var(--card-shadow)';
        });
        
        // Добавляем неоновый эффект для заголовков в карточках
        const cardTitle = card.querySelector('.card-title, .card-header');
        if (cardTitle) {
            cardTitle.classList.add('card-title-glow');
        }
    });
    
    // Специальные эффекты для dashboard карточек
    const dashboardCards = document.querySelectorAll('.dashboard-card');
    
    dashboardCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const icon = this.querySelector('.dashboard-icon');
            if (icon) {
                icon.style.animation = 'neonPulse 1.5s infinite';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            const icon = this.querySelector('.dashboard-icon');
            if (icon) {
                icon.style.animation = 'none';
            }
        });
    });
}

// Эффекты для таблиц
function initTableEffects() {
    const tables = document.querySelectorAll('.table');
    
    tables.forEach(table => {
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            row.addEventListener('mouseenter', function() {
                this.style.boxShadow = '0 0 10px rgba(142, 36, 170, 0.3)';
                this.style.backgroundColor = 'rgba(142, 36, 170, 0.1)';
                const cells = this.querySelectorAll('td');
                cells.forEach(cell => {
                    cell.style.color = 'var(--text-color)';
                });
            });
            
            row.addEventListener('mouseleave', function() {
                this.style.boxShadow = 'none';
                this.style.backgroundColor = '';
                const cells = this.querySelectorAll('td');
                cells.forEach(cell => {
                    cell.style.color = '';
                });
            });
        });
    });
}

// Проверка и обработка уведомлений
function checkNotifications() {
    const alerts = document.querySelectorAll('.alert');
    
    if (alerts.length > 0) {
        alerts.forEach(alert => {
            alert.classList.add('neon-border');
            
            if (alert.classList.contains('alert-success')) {
                alert.style.boxShadow = '0 0 10px rgba(0, 200, 83, 0.5)';
            } else if (alert.classList.contains('alert-danger')) {
                alert.style.boxShadow = '0 0 10px rgba(245, 0, 87, 0.5)';
            } else if (alert.classList.contains('alert-warning')) {
                alert.style.boxShadow = '0 0 10px rgba(255, 171, 0, 0.5)';
            } else if (alert.classList.contains('alert-info')) {
                alert.style.boxShadow = '0 0 10px rgba(124, 77, 255, 0.5)';
            }
            
            setTimeout(() => {
                alert.classList.add('fade-out');
                setTimeout(() => {
                    alert.remove();
                }, 500);
            }, 5000);
        });
    }
}

// Анимированная загрузка страницы
window.addEventListener('load', function() {
    const preloader = document.getElementById('preloader');
    if (preloader) {
        setTimeout(() => {
            preloader.style.opacity = '0';
            setTimeout(() => {
                preloader.style.display = 'none';
            }, 300);
        }, 500);
    }
});

// Настройки для Charts.js с темной темой
if (typeof Chart !== 'undefined') {
    Chart.defaults.color = '#b3b3b3';
    Chart.defaults.borderColor = 'rgba(142, 36, 170, 0.1)';
    
    // Кастомный градиент для графиков
    const createPurpleGradient = (ctx) => {
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(142, 36, 170, 0.8)');
        gradient.addColorStop(1, 'rgba(142, 36, 170, 0.1)');
        return gradient;
    };
    
    // Применение градиента ко всем графикам
    const originalLineController = Chart.controllers.line;
    Chart.controllers.line = Chart.controllers.line.extend({
        draw: function() {
            originalLineController.prototype.draw.apply(this, arguments);
            
            const ctx = this.chart.ctx;
            const _stroke = ctx.stroke;
            ctx.stroke = function() {
                ctx.save();
                ctx.shadowColor = 'rgba(142, 36, 170, 0.5)';
                ctx.shadowBlur = 10;
                ctx.shadowOffsetX = 0;
                ctx.shadowOffsetY = 0;
                _stroke.apply(this, arguments);
                ctx.restore();
            };
        }
    });
} 