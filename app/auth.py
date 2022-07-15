from flask import Flask
from flask import Blueprint, request, redirect, render_template, url_for
# from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
# from .model import RegisterForm, LoginForm, ResetForm,User
from flask_login import LoginManager, login_user, logout_user, current_user
from numpy import identity

from .database.db import accountdb, devicedb, roomdb
from .database.object import User, LoginForm
# from .model import User, LoginForm

auth = Blueprint('auth', __name__)

def check_login(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated: 
            return redirect(url_for('main'))
        return f(*args, **kwargs)
    return wrapper

def check_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or accountdb.checkAccountID(current_user.email) != "ADMIN": 
            return redirect(url_for('main'))
        return f(*args, **kwargs)
    return wrapper

@auth.route('/user-login', methods=['GET', 'POST'])
def userlogin():
    # print(accountID)
    if current_user.is_authenticated: 
        return redirect(url_for('user.main'))
    
    form = LoginForm()
    if request.method=='POST':
        if form.validate():
            email = form.email.data
            password = form.password.data
            loginInfo = accountdb.login(email, password, "USER")
            # print(check_password_hash(accountdb.checkAccountPw(email), password))
            # return(loginInfo)
            if "Login successfully!" in loginInfo:
                login_user(User(email=email))
                return redirect(url_for('user.main'))
            elif "Wrong Password!" in loginInfo:
                return render_template('user_login.html', form=form, pass_right=False, register=True)
            else:
                return render_template('user_login.html', form=form, pass_right=True, register=False)

    return render_template('user_login.html', form=form, pass_right=True, register=True)

@auth.route('/admin-login', methods=['GET', 'POST'])
def adminlogin():
    # print(accountID)
    if current_user.is_authenticated:
        if accountdb.checkAccountID(current_user.email) == "ADMIN": 
            return redirect(url_for('admin.main'))
    
    form = LoginForm()
    if request.method=='POST':
        if form.validate():
            email = form.email.data
            password = form.password.data
            loginInfo = accountdb.login(email, password, "ADMIN")
            # print(check_password_hash(accountdb.checkAccountPw(email), password))
            # return(loginInfo)
            if "Login successfully!" in loginInfo:
                login_user(User(email=email))
                return redirect(url_for('admin.main'))
            elif "Wrong Password!" in loginInfo:
                return render_template('admin_login.html', form=form, pass_right=False, register=True, authorized=True)
            elif "Not Authorized!" in loginInfo:
                return render_template('admin_login.html', form=form, pass_right=True, register=True, authorized=False)
            else:
                return render_template('admin_login.html', form=form, pass_right=True, register=False, authorized=True)

    return render_template('admin_login.html', form=form, pass_right=True, register=True, authorized=True)

@auth.route('/logout', methods=['GET', 'POST'])
@check_login
def logout():
    logout_user()
    accountdb.logout(current_user.email)
    return redirect(url_for('main'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    return "register"

@auth.route('/reset', methods=['GET', 'POST'])
def reset():
    return "reset"



