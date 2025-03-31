from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from app import db
from app.models.models import Order, OrderItem, MenuItem, Shift
from app.forms.waiter_forms import OrderForm, OrderItemForm
from datetime import datetime

waiter = Blueprint('waiter', __name__, url_prefix='/waiter')

def waiter_required(func):
    """Декоратор для проверки, что пользователь является официантом"""
    @login_required
    def decorated_view(*args, **kwargs):
        if current_user.role != 'waiter':
            flash('У вас нет прав доступа к этой странице')
            return redirect(url_for('auth.index'))
        return func(*args, **kwargs)
    decorated_view.__name__ = func.__name__
    return decorated_view

@waiter.route('/dashboard')
@waiter_required
def dashboard():
    # Получаем активную смену официанта
    active_shifts = [shift for shift in current_user.shifts if shift.status == 'active']
    active_shift = active_shifts[0] if active_shifts else None
    
    # Получаем заказы официанта в текущей смене
    if active_shift:
        orders = Order.query.filter_by(waiter_id=current_user.id, shift_id=active_shift.id).order_by(Order.created_at.desc()).all()
    else:
        orders = []
    
    return render_template('waiter/dashboard.html', title='Панель официанта', orders=orders, active_shift=active_shift)

@waiter.route('/orders')
@waiter_required
def orders_list():
    # Получаем все заказы официанта
    orders = Order.query.filter_by(waiter_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('waiter/orders_list.html', title='Мои заказы', orders=orders)

@waiter.route('/orders/new', methods=['GET', 'POST'])
@waiter_required
def create_order():
    # Проверяем, есть ли активная смена
    active_shifts = [shift for shift in current_user.shifts if shift.status == 'active']
    if not active_shifts:
        flash('Невозможно создать заказ - у вас нет активной смены')
        return redirect(url_for('waiter.dashboard'))
    
    form = OrderForm()
    
    if form.validate_on_submit():
        order = Order(
            table_number=form.table_number.data,
            status='new',
            created_at=datetime.utcnow(),
            waiter_id=current_user.id,
            shift_id=active_shifts[0].id
        )
        db.session.add(order)
        db.session.commit()
        
        flash(f'Заказ #{order.id} успешно создан')
        return redirect(url_for('waiter.add_items', order_id=order.id))
    
    return render_template('waiter/order_form.html', title='Новый заказ', form=form)

@waiter.route('/orders/<int:order_id>/add_items', methods=['GET', 'POST'])
@waiter_required
def add_items(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Проверяем, является ли текущий пользователь официантом этого заказа
    if order.waiter_id != current_user.id:
        flash('Вы не можете редактировать этот заказ')
        return redirect(url_for('waiter.orders_list'))
    
    # Проверяем, можно ли добавлять позиции (только для новых заказов)
    if order.status not in ['new', 'in_progress']:
        flash('Нельзя изменять заказ в этом статусе')
        return redirect(url_for('waiter.order_details', order_id=order.id))
    
    form = OrderItemForm()
    
    # Заполняем выпадающий список доступными пунктами меню
    form.menu_item_id.choices = [(item.id, f"{item.name} - {item.price} ₽") 
                                for item in MenuItem.query.filter_by(status='available').all()]
    
    if form.validate_on_submit():
        # Проверяем, не добавлен ли уже этот пункт меню в заказ
        existing_item = OrderItem.query.filter_by(
            order_id=order.id,
            menu_item_id=form.menu_item_id.data
        ).first()
        
        if existing_item:
            # Обновляем количество
            existing_item.quantity += form.quantity.data
            db.session.commit()
            flash('Позиция обновлена в заказе')
        else:
            # Добавляем новую позицию
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=form.menu_item_id.data,
                quantity=form.quantity.data,
                status='pending'
            )
            db.session.add(order_item)
            db.session.commit()
            flash('Позиция добавлена в заказ')
        
        # Устанавливаем флаг в сессии для отображения уведомления
        session['item_added'] = True
        
        if request.form.get('add_more'):
            return redirect(url_for('waiter.add_items', order_id=order.id))
        else:
            return redirect(url_for('waiter.order_details', order_id=order.id))
    
    return render_template('waiter/add_item.html', title=f'Добавление позиций в заказ #{order.id}', form=form, order=order)

@waiter.route('/orders/<int:order_id>')
@waiter_required
def order_details(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Проверяем, является ли текущий пользователь официантом этого заказа
    if order.waiter_id != current_user.id:
        flash('Вы не можете просматривать этот заказ')
        return redirect(url_for('waiter.orders_list'))
    
    # Получаем значение флага из сессии и сразу удаляем его
    item_added = session.pop('item_added', False)
    
    return render_template('waiter/order_details.html', title=f'Заказ #{order.id}', order=order)

@waiter.route('/orders/<int:order_id>/update_status', methods=['POST'])
@waiter_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Проверяем, является ли текущий пользователь официантом этого заказа
    if order.waiter_id != current_user.id:
        flash('Вы не можете изменять этот заказ')
        return redirect(url_for('waiter.orders_list'))
    
    new_status = request.form.get('status')
    
    if new_status in ['new', 'in_progress', 'completed']:
        # Если заказ завершается, устанавливаем дату завершения
        if new_status == 'completed' and order.status != 'completed':
            order.completed_at = datetime.utcnow()
        
        order.status = new_status
        db.session.commit()
        flash(f'Статус заказа изменен на "{new_status}"')
    else:
        flash('Некорректный статус')
    
    return redirect(url_for('waiter.order_details', order_id=order.id))

@waiter.route('/orders/<int:order_id>/remove_item/<int:item_id>', methods=['POST'])
@waiter_required
def remove_item(order_id, item_id):
    order = Order.query.get_or_404(order_id)
    order_item = OrderItem.query.get_or_404(item_id)
    
    # Проверяем, является ли текущий пользователь официантом этого заказа
    if order.waiter_id != current_user.id:
        flash('Вы не можете изменять этот заказ')
        return redirect(url_for('waiter.orders_list'))
    
    # Проверяем, что позиция принадлежит заказу
    if order_item.order_id != order.id:
        flash('Позиция не принадлежит этому заказу')
        return redirect(url_for('waiter.order_details', order_id=order.id))
    
    # Проверяем, можно ли удалять позиции (только для новых заказов)
    if order.status != 'new':
        flash('Нельзя изменять заказ в этом статусе')
        return redirect(url_for('waiter.order_details', order_id=order.id))
    
    db.session.delete(order_item)
    db.session.commit()
    flash('Позиция удалена из заказа')
    
    return redirect(url_for('waiter.order_details', order_id=order.id)) 