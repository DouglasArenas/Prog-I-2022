
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms import validators

class LoginForm(FlaskForm):

    email = EmailField('E-mail',
    [
        validators.Required(message = "El correo es requerido"),
        validators.Email( message ='Formato no válido'),
    ],
    render_kw={"placeholder": "Email"}
    )

    #Definición de campo de contraseña
    password = PasswordField('Contraseña', [
        validators.Required(),
    ],
    render_kw={"placeholder": "Password"}
    )
    #Definición de campo submit
    submit = SubmitField("Send")