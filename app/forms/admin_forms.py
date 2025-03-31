from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, DateField, TimeField, SelectMultipleField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError, Email, Optional, EqualTo
from app.models.models import User

class UserForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=4, max=64)])
    full_name = StringField('Полное имя', validators=[DataRequired(), Length(max=128)])
    password = PasswordField('Пароль', validators=[Optional(), Length(min=6, max=64)])
    role = SelectField('Роль', choices=[('admin', 'Администратор'), ('waiter', 'Официант'), ('cook', 'Повар')], validators=[DataRequired()])
    submit = SubmitField('Сохранить')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None and getattr(self, 'id', None) != user.id:
            raise ValidationError('Это имя пользователя уже занято.')

class ShiftForm(FlaskForm):
    date = DateField('Дата', validators=[DataRequired()], format='%Y-%m-%d')
    start_time = TimeField('Время начала', validators=[DataRequired()], format='%H:%M')
    end_time = TimeField('Время окончания', validators=[DataRequired()], format='%H:%M')
    users = SelectMultipleField('Сотрудники', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Сохранить')

class MenuItemForm(FlaskForm):
    name = StringField('Название блюда', validators=[DataRequired(), Length(min=2, max=100)])
    price = FloatField('Цена (руб.)', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Сохранить') 