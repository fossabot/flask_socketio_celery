from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from apps.extensions import login_manager
from apps.auth.forms import LoginForm, RegisterForm
from apps.auth.models import User
from apps.utils import flash_errors

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


@blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('登录成功', 'success')
            redirect_url = request.args.get('next') or url_for('public.index')
            return redirect(redirect_url)
        else:
            flash_errors(form, category='danger')
    return render_template('auth/login.html', form=form)


@blueprint.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(
            username=form.username.data,
            password=form.password.data,
            active=True)
        flash('注册成功，请登录', 'success')
        return redirect(url_for('public.index'))
    else:
        flash_errors(form)
    return render_template('auth/signup.html', form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('退出成功', 'info')
    return redirect(url_for('public.index'))
