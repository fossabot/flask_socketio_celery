"""User forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, Length
from .models import User


class RegisterForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(),
                                Length(min=3, max=25)])
    password = PasswordField(
        'Password', validators=[DataRequired(),
                                Length(min=6, max=40)])
    confirm = PasswordField(
        'Verify password',
        [DataRequired(), EqualTo('password', message='密码必须相同')])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('用户名已被使用')
            return False
        user = User.query.filter_by(email=self.email.data).first()
        return True


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append('用户不存在')
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append('密码错误')
            return False

        if not self.user.active:
            self.username.errors.append('用户未激活')
            return False
        return True
