from app import create_app, db
from app.models.models import User, Shift, Order, MenuItem, OrderItem
from datetime import datetime, date, time
import os

app = create_app()

# Создание контекста приложения для работы с базой данных
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Shift': Shift, 
        'Order': Order, 
        'MenuItem': MenuItem, 
        'OrderItem': OrderItem
    }

def init_test_data():
    """Инициализация тестовых данных"""
    # Проверяем наличие тестовых пользователей
    if User.query.count() == 0:
        # Добавляем администратора
        admin = User(
            username='admin',
            full_name='Администратор',
            role='admin',
            status='active'
        )
        admin.set_password('admin123')
        
        # Добавляем официанта
        waiter = User(
            username='waiter',
            full_name='Иванов Иван',
            role='waiter',
            status='active'
        )
        waiter.set_password('waiter123')
        
        # Добавляем повара
        cook = User(
            username='cook',
            full_name='Петров Петр',
            role='cook',
            status='active'
        )
        cook.set_password('cook123')
        
        db.session.add_all([admin, waiter, cook])
        db.session.commit()
    
    # Добавляем пункты меню, если их нет
    if MenuItem.query.count() == 0:
        menu_items = [
            MenuItem(name='Капучино', description='Классический кофейный напиток', price=150, category='Напитки', status='available'),
            MenuItem(name='Латте', description='Кофе с молоком', price=170, category='Напитки', status='available'),
            MenuItem(name='Эспрессо', description='Крепкий кофе', price=120, category='Напитки', status='available'),
            MenuItem(name='Чай зеленый', description='Классический зеленый чай', price=100, category='Напитки', status='available'),
            MenuItem(name='Чай черный', description='Классический черный чай', price=100, category='Напитки', status='available'),
            
            MenuItem(name='Цезарь с курицей', description='Салат с курицей, сыром и соусом', price=350, category='Салаты', status='available'),
            MenuItem(name='Греческий салат', description='Салат с овощами, сыром фета и оливками', price=320, category='Салаты', status='available'),
            MenuItem(name='Оливье', description='Традиционный салат с майонезом', price=280, category='Салаты', status='available'),
            
            MenuItem(name='Карбонара', description='Паста с беконом и сливочным соусом', price=420, category='Горячие блюда', status='available'),
            MenuItem(name='Стейк из говядины', description='Сочный стейк с гарниром', price=650, category='Горячие блюда', status='available'),
            MenuItem(name='Куриное филе на гриле', description='С овощами и соусом', price=380, category='Горячие блюда', status='available'),
            MenuItem(name='Рыба запеченная', description='Филе белой рыбы с овощами', price=450, category='Горячие блюда', status='available'),
            
            MenuItem(name='Картофель фри', description='Хрустящий картофель', price=150, category='Гарниры', status='available'),
            MenuItem(name='Рис отварной', description='С зеленью и маслом', price=120, category='Гарниры', status='available'),
            MenuItem(name='Овощи гриль', description='Ассорти сезонных овощей', price=180, category='Гарниры', status='available'),
            
            MenuItem(name='Тирамису', description='Итальянский десерт с кофе', price=220, category='Десерты', status='available'),
            MenuItem(name='Чизкейк', description='Классический десерт с ягодами', price=250, category='Десерты', status='available'),
            MenuItem(name='Мороженое', description='Ванильное с топпингом', price=150, category='Десерты', status='available'),
        ]
        
        db.session.add_all(menu_items)
        db.session.commit()

# Инициализация базы данных и создание тестовых данных
def init_db():
    """Создание базы данных и инициализация тестовых данных"""
    print("Инициализация базы данных...")
    # Убедимся, что директория instance существует
    try:
        print(f"Проверка директории instance: {app.instance_path}")
        os.makedirs(app.instance_path, exist_ok=True)
        print(f"Директория создана или уже существует")
    except Exception as e:
        print(f"Ошибка при создании директории: {e}")
        
    with app.app_context():
        print("Создание таблиц базы данных...")
        db.create_all()
        print("Инициализация тестовых данных...")
        init_test_data()
        print("Инициализация базы данных завершена успешно!")

if __name__ == '__main__':
    # Инициализация базы данных перед запуском приложения
    init_db()
    app.run(debug=True) 