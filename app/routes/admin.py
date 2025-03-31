from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.models import User, Shift, Order, MenuItem, OrderItem
from app.forms.admin_forms import UserForm, ShiftForm, MenuItemForm
from datetime import datetime, timedelta
from sqlalchemy import func, desc, and_

admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(func):
    """Декоратор для проверки, что пользователь является администратором"""
    @login_required
    def decorated_view(*args, **kwargs):
        if current_user.role != 'admin':
            flash('У вас нет прав доступа к этой странице')
            return redirect(url_for('auth.index'))
        return func(*args, **kwargs)
    decorated_view.__name__ = func.__name__
    return decorated_view

@admin.route('/dashboard')
@admin_required
def dashboard():
    """Панель управления администратора с реальными метриками."""
    from app.models.models import User, Order, MenuItem, OrderItem
    from sqlalchemy import func, desc, and_
    from datetime import datetime, timedelta
    
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    week_ago = today - timedelta(days=7)
    
    # Активные заказы (статус: new, processing, ready)
    active_orders = Order.query.filter(Order.status.in_(['new', 'processing', 'ready'])).count()
    
    # Расчет изменения активных заказов по сравнению с прошлой неделей
    week_ago_active_orders = Order.query.filter(
        and_(
            Order.status.in_(['new', 'processing', 'ready']),
            func.date(Order.created_at) == week_ago
        )
    ).count()
    
    if week_ago_active_orders > 0:
        active_orders_change = ((active_orders - week_ago_active_orders) / week_ago_active_orders) * 100
    else:
        active_orders_change = 0
    
    # Официанты на активной смене
    active_waiters = User.query.filter_by(role='waiter', status='active').join(
        User.shifts
    ).filter(
        Shift.date == today,
        Shift.status == 'active'
    ).count()
    
    # Расчет изменения количества официантов по сравнению с прошлой неделей
    week_ago_active_waiters = User.query.filter_by(role='waiter', status='active').join(
        User.shifts
    ).filter(
        Shift.date == week_ago,
        Shift.status == 'active'
    ).count()
    
    if week_ago_active_waiters > 0:
        waiters_change = ((active_waiters - week_ago_active_waiters) / week_ago_active_waiters) * 100
    else:
        waiters_change = 0
    
    # Расчет выручки за сегодня
    today_orders = Order.query.filter(
        func.date(Order.created_at) == today
    ).all()
    
    today_revenue = 0
    for order in today_orders:
        for item in order.items:
            today_revenue += item.menu_item.price * item.quantity
    
    # Расчет выручки за вчера
    yesterday_orders = Order.query.filter(
        func.date(Order.created_at) == yesterday
    ).all()
    
    yesterday_revenue = 0
    for order in yesterday_orders:
        for item in order.items:
            yesterday_revenue += item.menu_item.price * item.quantity
    
    # Расчет изменения выручки
    if yesterday_revenue > 0:
        revenue_change = ((today_revenue - yesterday_revenue) / yesterday_revenue) * 100
    else:
        revenue_change = 0
    
    # Количество блюд в меню
    menu_items_count = MenuItem.query.filter_by(status='available').count()
    
    # Получаем последние заказы
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    # Вычисляем сумму каждого заказа
    for order in recent_orders:
        total_price = 0
        for item in order.items:
            total_price += item.menu_item.price * item.quantity
        order.total_price = total_price
    
    # Добавляем статусы и цвета для отображения
    for order in recent_orders:
        if order.status == 'new':
            order.status_display = 'Новый'
            order.status_color = 'info'
        elif order.status == 'processing':
            order.status_display = 'Готовится'
            order.status_color = 'warning'
        elif order.status == 'ready':
            order.status_display = 'Готов'
            order.status_color = 'success'
        elif order.status == 'completed':
            order.status_display = 'Завершен'
            order.status_color = 'primary'
        elif order.status == 'canceled':
            order.status_display = 'Отменен'
            order.status_color = 'danger'
    
    # Получаем популярные блюда (топ-5)
    popular_dishes = db.session.query(
        MenuItem.name,
        func.sum(OrderItem.quantity).label('total_ordered')
    ).join(
        OrderItem,
        MenuItem.id == OrderItem.menu_item_id
    ).group_by(
        MenuItem.name
    ).order_by(
        desc('total_ordered')
    ).limit(5).all()
    
    # Получаем данные для графика заказов за последнюю неделю
    last_week_dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
    last_week_orders_count = []
    last_week_revenue = []
    
    for date_str in last_week_dates:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Количество заказов за этот день
        day_orders_count = Order.query.filter(
            func.date(Order.created_at) == date_obj
        ).count()
        last_week_orders_count.append(day_orders_count)
        
        # Выручка за этот день
        day_orders = Order.query.filter(
            func.date(Order.created_at) == date_obj
        ).all()
        
        day_revenue = 0
        for order in day_orders:
            for item in order.items:
                day_revenue += item.menu_item.price * item.quantity
        
        last_week_revenue.append(day_revenue)
    
    # Получаем недавние действия (логи активности)
    recent_activity = []
    
    # Последние созданные заказы
    recent_created_orders = Order.query.order_by(Order.created_at.desc()).limit(3).all()
    for order in recent_created_orders:
        waiter_name = order.waiter.full_name if order.waiter else 'Неизвестный'
        time_ago = (datetime.now() - order.created_at).total_seconds() / 60
        activity = {
            'type': 'order',
            'content': f'Новый заказ #{order.id} был создан официантом {waiter_name}',
            'time_ago': int(time_ago),
            'timestamp': order.created_at
        }
        recent_activity.append(activity)
    
    # Последние добавленные пользователи
    recent_users = User.query.order_by(User.created_at.desc()).limit(2).all()
    for user in recent_users:
        time_ago = (datetime.now() - user.created_at).total_seconds() / 60
        activity = {
            'type': 'user',
            'content': f'Новый сотрудник {user.full_name} ({user.role}) был добавлен в систему',
            'time_ago': int(time_ago),
            'timestamp': user.created_at
        }
        recent_activity.append(activity)
    
    # Сортируем активность по времени
    recent_activity.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return render_template(
        'admin/dashboard.html',
        active_orders=active_orders,
        active_orders_change=active_orders_change,
        active_waiters=active_waiters,
        waiters_change=waiters_change,
        today_revenue=int(today_revenue),
        revenue_change=revenue_change,
        menu_items_count=menu_items_count,
        recent_orders=recent_orders,
        popular_dishes=popular_dishes,
        chart_dates=last_week_dates,
        chart_orders=last_week_orders_count,
        chart_revenue=last_week_revenue,
        recent_activity=recent_activity
    )

# Управление пользователями
@admin.route('/users')
@admin_required
def users_list():
    users = User.query.all()
    return render_template('admin/users_list.html', title='Список сотрудников', users=users)

@admin.route('/users/add', methods=['GET', 'POST'])
@admin_required
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            full_name=form.full_name.data,
            role=form.role.data,
            status='active'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Сотрудник успешно добавлен')
        return redirect(url_for('admin.users_list'))
    return render_template('admin/user_form.html', title='Добавление сотрудника', form=form)

@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash('Информация о сотруднике обновлена')
        return redirect(url_for('admin.users_list'))
    return render_template('admin/user_form.html', title='Редактирование сотрудника', form=form, user=user)

@admin.route('/users/<int:user_id>/toggle_status', methods=['POST'])
@admin_required
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    if user.status == 'active':
        user.status = 'fired'
        flash(f'Сотрудник {user.full_name} отмечен как уволенный')
    else:
        user.status = 'active'
        flash(f'Сотрудник {user.full_name} восстановлен')
    db.session.commit()
    return redirect(url_for('admin.users_list'))

# Управление меню
@admin.route('/menu')
@admin_required
def menu_list():
    menu_items = MenuItem.query.all()
    return render_template('admin/menu_list.html', title='Меню', menu_items=menu_items)

@admin.route('/menu/add', methods=['GET', 'POST'])
@admin_required
def add_menu_item():
    form = MenuItemForm()
    if form.validate_on_submit():
        menu_item = MenuItem(
            name=form.name.data,
            category='main',  # Устанавливаем категорию по умолчанию
            price=form.price.data,
            description=form.description.data
        )
        db.session.add(menu_item)
        db.session.commit()
        flash('Блюдо успешно добавлено в меню', 'success')
        return redirect(url_for('admin.menu_list'))
    return render_template('admin/menu_form.html', title='Добавление блюда', form=form)

@admin.route('/menu/<int:item_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_menu_item(item_id):
    menu_item = MenuItem.query.get_or_404(item_id)
    form = MenuItemForm(obj=menu_item)
    if form.validate_on_submit():
        menu_item.name = form.name.data
        menu_item.price = form.price.data
        menu_item.description = form.description.data
        # Сохраняем существующую категорию
        db.session.commit()
        flash('Информация о блюде обновлена', 'success')
        return redirect(url_for('admin.menu_list'))
    return render_template('admin/menu_form.html', title='Редактирование блюда', form=form, menu_item=menu_item)

@admin.route('/menu/<int:item_id>/delete', methods=['POST'])
@admin_required
def delete_menu_item(item_id):
    menu_item = MenuItem.query.get_or_404(item_id)
    db.session.delete(menu_item)
    db.session.commit()
    flash(f'Блюдо "{menu_item.name}" удалено из меню', 'success')
    return redirect(url_for('admin.menu_list'))

# Управление сменами
@admin.route('/shifts')
@admin_required
def shifts_list():
    shifts = Shift.query.order_by(Shift.date.desc()).all()
    return render_template('admin/shifts_list.html', title='Список смен', shifts=shifts)

@admin.route('/shifts/add', methods=['GET', 'POST'])
@admin_required
def add_shift():
    form = ShiftForm()
    form.users.choices = [(u.id, u.full_name) for u in User.query.filter_by(status='active').all()]
    
    if form.validate_on_submit():
        shift = Shift(
            date=form.date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            status='active'
        )
        db.session.add(shift)
        db.session.commit()
        
        # Добавление сотрудников в смену
        for user_id in form.users.data:
            user = User.query.get(user_id)
            shift.users.append(user)
        
        db.session.commit()
        flash('Смена успешно создана')
        return redirect(url_for('admin.shifts_list'))
    
    return render_template('admin/shift_form.html', title='Создание смены', form=form)

@admin.route('/shifts/<int:shift_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_shift(shift_id):
    shift = Shift.query.get_or_404(shift_id)
    form = ShiftForm(obj=shift)
    form.users.choices = [(u.id, u.full_name) for u in User.query.filter_by(status='active').all()]
    
    if form.validate_on_submit():
        # Обновляем основные поля, кроме users
        shift.date = form.date.data
        shift.start_time = form.start_time.data
        shift.end_time = form.end_time.data
        
        # Обновление сотрудников в смене
        shift.users = []
        for user_id in form.users.data:
            user = User.query.get(user_id)
            if user:  # Проверяем, что пользователь существует
                shift.users.append(user)
        
        db.session.commit()
        flash('Информация о смене обновлена')
        return redirect(url_for('admin.shifts_list'))
    
    # Предварительно выбрать текущих пользователей смены
    form.users.data = [user.id for user in shift.users]
    
    return render_template('admin/shift_form.html', title='Редактирование смены', form=form, shift=shift)

# Просмотр заказов
@admin.route('/orders')
@admin_required
def orders_list():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders_list.html', title='Список заказов', orders=orders)

@admin.route('/orders/<int:order_id>')
@admin_required
def order_details(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_details.html', title=f'Заказ #{order.id}', order=order) 