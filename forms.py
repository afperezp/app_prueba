from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField,TextAreaField, DateField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, Length, EqualTo



class RegisterForm (FlaskForm):
    first = StringField('Nombre:', validators=[DataRequired()])
    username = StringField('Apodo del colegio', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max= 20)])
    confirm_password = PasswordField('repite esa verga', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Pila')
class LoginForm (FlaskForm):
    username = StringField('Apodo', validators=[DataRequired(), Length(min=2)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit  = SubmitField('logineate pila')
    
class PostForm(FlaskForm):
    title =  StringField('un titulo sucia', validators=[DataRequired()])
    content =  TextAreaField('Escribe aca lo q se te plazca en gana', validators=[DataRequired()])
    submit = SubmitField('Postea  esa caga')
class EventosForm(FlaskForm):
    name = StringField('Como se llamaba el  evento:', validators=[DataRequired()])
    descripcion = StringField('una pequeña descripcion:',  validators=[DataRequired()])
    fecha = DateField('Mas o menos cuando fue el evento', validators=[DataRequired()])
    submit = SubmitField('crea esa caga')

class UpdateForm(FlaskForm):
    username = StringField('Apodo', validators=[DataRequired(), Length(min=2)])
    first = StringField('Nombre:', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','jpeg', 'png', 'HEIC'])])
    submit = SubmitField('crea esa caga')

    
