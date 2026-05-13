from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import Email, InputRequired, Length


class RegisterForm(FlaskForm):
    email = StringField(
        "Email",
        description="Your school email address",
        validators=[InputRequired(), Email(), Length(max=50)]
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=4)]
    )
    role = SelectField(
        "Role",
        choices=[("viewer", "Viewer"), ("admin", "Admin")]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")
