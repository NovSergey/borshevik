from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, FloatField
from wtforms.validators import DataRequired

from flask_wtf.file import FileRequired, FileAllowed, FileField
class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class AddPolygon(FlaskForm):
    file = FileField('Вставте фото (Не обязятельно)', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    coords = StringField('Координаты', validators=[DataRequired()])
    submit = SubmitField('Сохранить область')