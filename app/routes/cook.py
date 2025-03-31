from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.models import Order, OrderItem, User
from datetime import datetime

cook = Blueprint('cook', __name__, url_prefix='/cook')

def cook_required(func):
    """Декоратор для проверки, что пользователь является поваром"""
    @login_required
    def decorated_view(*args, **kwargs):
        if current_user.role != 'cook':
            flash('У вас нет прав доступа к этой странице')
            return redirect(url_for('auth.index'))
        return func(*args, **kwargs)
    decorated_view.__name__ = func.__name__
    return decorated_view

@cook.route('/dashboard')
@cook_required
def dashboard():
    # Получаем активные заказы для отображения на дашборде
    recent_orders = Order.query.filter(Order.status.in_(['new', 'in_progress'])).order_by(Order.created_at.desc()).limit(5).all()
    return render_template('cook/dashboard.html', title='Панель повара', recent_orders=recent_orders)

@cook.route('/orders')
@cook_required
def orders_list():
    # Получаем заказы со статусом "new" и "in_progress"
    orders = Order.query.filter(Order.status.in_(['new', 'in_progress'])).order_by(Order.created_at.desc()).all()
    
    # Получаем список активных официантов для фильтра
    waiters = User.query.filter_by(role='waiter', status='active').all()
    
    return render_template('cook/orders_list.html', title='Список активных заказов', orders=orders, waiters=waiters)

@cook.route('/orders/<int:order_id>')
@cook_required
def order_details(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('cook/order_details.html', title=f'Заказ #{order.id}', order=order)

@cook.route('/order_items/<int:item_id>/update_status', methods=['POST'])
@cook_required
def update_item_status(item_id):
    order_item = OrderItem.query.get_or_404(item_id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'preparing', 'ready']:
        order_item.status = new_status
        db.session.commit()
        
        # Проверяем, все ли позиции заказа готовы
        order = order_item.order
        all_items_ready = all(item.status == 'ready' for item in order.items)
        
        # Если все позиции готовы, меняем статус заказа
        if all_items_ready and order.status != 'completed':
            order.status = 'in_progress'
            db.session.commit()
            
        flash(f'Статус позиции заказа #{order.id} изменен на "{new_status}"')
    else:
        flash('Некорректный статус')
    
    return redirect(url_for('cook.order_details', order_id=order_item.order_id)) 