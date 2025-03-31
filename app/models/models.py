from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    full_name = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20))  # admin, waiter, cook
    status = db.Column(db.String(20), default='active')  # active, fired
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    shifts = db.relationship('Shift', secondary='user_shift', back_populates='users')
    orders = db.relationship('Order', backref='waiter', foreign_keys='Order.waiter_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'
        
class Shift(db.Model):
    __tablename__ = 'shifts'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='active')
    
    users = db.relationship('User', secondary='user_shift', back_populates='shifts')
    orders = db.relationship('Order', backref='shift')
    
    def __repr__(self):
        return f'<Shift {self.date} {self.start_time}-{self.end_time}>'
        
user_shift = db.Table('user_shift',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('shift_id', db.Integer, db.ForeignKey('shifts.id'), primary_key=True)
)

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='new')  # new, in_progress, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    waiter_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    shift_id = db.Column(db.Integer, db.ForeignKey('shifts.id'))
    
    items = db.relationship('OrderItem', backref='order')
    
    def __repr__(self):
        return f'<Order {self.id}>'
        
class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(64))
    status = db.Column(db.String(20), default='available')  # available, unavailable
    
    def __repr__(self):
        return f'<MenuItem {self.name}>'
        
class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'))
    quantity = db.Column(db.Integer, default=1)
    status = db.Column(db.String(20), default='pending')  # pending, preparing, ready
    
    menu_item = db.relationship('MenuItem')
    
    def __repr__(self):
        return f'<OrderItem {self.menu_item.name} x{self.quantity}>' 