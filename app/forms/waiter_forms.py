from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, ValidationError

class OrderForm(FlaskForm):
    table_number = IntegerField('Номер стола', validators=[
        DataRequired(),
        NumberRange(min=1, max=100, message='Номер стола должен быть от 1 до 100')
    ])
    submit = SubmitField('Создать заказ')

class OrderItemForm(FlaskForm):
    menu_item_id = SelectField('Позиция меню', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Количество', validators=[
        DataRequired(),
        NumberRange(min=1, max=20, message='Количество должно быть от 1 до 20')
    ])
    submit = SubmitField('Добавить в заказ') 