from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from src.accounts.models import UserAccountTable


# Defines login form layout and restraints
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


# Defines registration form layout and restraints
class RegisterForm(FlaskForm):
    email = EmailField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    role = SelectField(
        "Role",
        validators=[DataRequired()],
        choices=[('emp', 'Employee'), ('mgr', 'Manager')]
    )

    def validate(self, extra_validators=None):
        initial_validation = super(RegisterForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        user = UserAccountTable.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match")
            return False
        return True
