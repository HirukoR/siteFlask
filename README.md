# Кафе Система - Приложение для управления кафе

Современное веб-приложение для комплексного управления кафе с красивым UI/UX дизайном. Система предназначена для автоматизации всех ключевых процессов в заведении общественного питания, включая управление заказами, работу кухни и администрирование.

## Обзор функционала

### Администратор
- Полное управление персоналом (регистрация сотрудников, увольнение, просмотр статистики)
- Создание и редактирование меню (добавление блюд, изменение цен, категорий)
- Управление столиками (добавление, удаление, изменение статуса)
- Назначение сотрудников на смены
- Просмотр финансовых отчетов и статистики работы заведения
- Мониторинг всех заказов и операций в системе

### Официант
- Прием и оформление заказов от клиентов
- Передача заказов на кухню
- Отслеживание статуса выполнения заказов
- Закрытие заказов и формирование счета
- Управление заказами для своих столиков
- Просмотр истории обслуженных заказов

### Повар
- Просмотр новых и активных заказов
- Обновление статусов блюд (в процессе приготовления, готово)
- Управление очередью заказов
- Визуализация прогресса выполнения заказа
- Получение уведомлений о новых заказах
- Отслеживание эффективности работы кухни

## Технические особенности
- Современный адаптивный дизайн с темной темой и неоновыми акцентами
- Анимации и визуальные эффекты для улучшения пользовательского опыта
- Интерактивные таблицы с возможностью сортировки и фильтрации
- Прогресс-бары и графические элементы для отображения статусов
- Система уведомлений о новых событиях
- Подробная статистика и визуализация данных

## Технологический стек

### Бэкенд
- Python 3.8+
- Flask 2.0.3 - веб-фреймворк
- SQLAlchemy 1.4 - ORM для работы с базой данных
- Flask-Login - управление пользовательскими сессиями
- Flask-WTF - создание и валидация форм
- Flask-Migrate - миграции базы данных
- SQLite - СУБД для хранения данных

### Фронтенд
- HTML5, CSS3, JavaScript
- Bootstrap 5 - фреймворк для создания адаптивного UI
- Chart.js - библиотека для создания графиков
- Custom CSS с анимациями и градиентами
- Адаптивная верстка для всех устройств

## Установка и запуск

### Требования
- Python 3.8 или выше
- pip (менеджер пакетов Python)
- Git (опционально, для клонирования репозитория)

### Шаги установки

1. Клонируйте репозиторий или распакуйте архив с проектом:
```bash
git clone <url_репозитория>
cd <папка_проекта>
```

2. Создайте и активируйте виртуальное окружение:
```bash
# Создание виртуального окружения
py -m venv venv

# Активация в Bash
source venv/Scripts/activate
```

3. Установите все зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте папку для базы данных и запустите инициализацию:
```bash
# Создание директории для базы данных
mkdir -p instance

# Запуск приложения для инициализации базы
py run.py
```

5. Запустите приложение:
```bash
py run.py
```

6. Откройте браузер и перейдите по адресу: http://127.0.0.1:5000

### Учетные данные по умолчанию

После первого запуска автоматически создаются тестовые аккаунты:

- **Администратор**:
  - Логин: admin
  - Пароль: admin123

- **Официант**:
  - Логин: waiter
  - Пароль: waiter123

- **Повар**:
  - Логин: cook
  - Пароль: cook123

## Структура проекта

```
cafe_system/
├── app/                      # Основной пакет приложения
│   ├── __init__.py           # Инициализация приложения
│   ├── models/               # Модели базы данных
│   │   └── models.py         # Определения всех моделей
│   ├── routes/               # Маршруты и контроллеры
│   │   ├── admin.py          # Функционал администратора
│   │   ├── auth.py           # Аутентификация и авторизация
│   │   ├── cook.py           # Функционал повара
│   │   ├── main.py           # Основные маршруты
│   │   └── waiter.py         # Функционал официанта
│   ├── forms/                # Формы ввода данных
│   ├── templates/            # HTML шаблоны
│   │   ├── admin/            # Шаблоны для админ-панели
│   │   ├── auth/             # Шаблоны аутентификации
│   │   ├── cook/             # Шаблоны для поваров
│   │   ├── waiter/           # Шаблоны для официантов
│   │   └── base.html         # Базовый шаблон сайта
│   └── static/               # Статические файлы
│       ├── css/              # CSS стили
│       ├── js/               # JavaScript файлы
│       └── img/              # Изображения
├── instance/                 # Папка с базой данных
│   └── cafe.db               # SQLite база данных
├── run.py                    # Скрипт запуска приложения
├── requirements.txt          # Зависимости проекта
└── README.md                 # Документация проекта
```

## Функциональные возможности

### Модуль администратора
- Управление пользователями: создание, редактирование, блокировка
- Управление меню: добавление, редактирование, удаление позиций
- Управление категориями блюд
- Настройка столиков и зон обслуживания
- Просмотр всех заказов с возможностью фильтрации
- Аналитика продаж и популярности блюд
- Формирование отчетов

### Модуль официанта
- Управление столиками и заказами
- Создание новых заказов с выбором блюд из меню
- Редактирование существующих заказов
- Отслеживание статуса готовности блюд
- Закрытие заказов и формирование счетов
- Печать чеков (имитация)

### Модуль повара
- Панель управления с активными заказами
- Изменение статуса блюд в заказах
- Визуализация прогресса выполнения заказов
- Просмотр деталей заказа
- Система приоритетов для заказов

## Разработка и расширение

### Запуск в режиме разработки
```bash
# Установка дополнительных пакетов для разработки
pip install pytest flask-testing

# Запуск в режиме отладки
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows
py run.py
```

### Миграции базы данных
```bash
# Инициализация миграций
flask db init

# Создание новой миграции
flask db migrate -m "описание изменений"

# Применение миграций
flask db upgrade
```



