from flask import Flask
from flask import Blueprint, request, redirect, render_template, url_for
# from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
# from .model import RegisterForm, LoginForm, ResetForm,User
from flask_login import LoginManager, login_user, logout_user, current_user
from numpy import identity

from .database.db import accountdb, systemdb, roomdb
from .database.utils import User, LoginForm, RegisterForm, ResetForm
from werkzeug.security import generate_password_hash, check_password_hash
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
    accountdb.logout(current_user.email)
    logout_user()
    return redirect(url_for('main'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form=RegisterForm()
    if request.method=='POST':
        if form.validate():
            email=form.email.data
            password=form.password.data
            passwordRepeat=form.passwordRepeat.data
            if not password == passwordRepeat:
                return render_template('register.html', form=form, exist=False, repeat=True)
            
            # exist=User.objects(email=email).first()
            account = accountdb.findUser(email)
            if account is None:
                # hashpassword=generate_password_hash(password, method='sha256')
                # user=User(username=username, password=hashpassword, email=email, room=room, roles=roles).save()
                accountdb.register(email, password)
                login_user(User(email=email))
                #return form.username.data+' '+form.email.data+' '+form.room.data+' '+form.password.data+' '+form.roles.data
                return redirect(url_for('main'))
            else:
                login_user(User(email=email))
                return render_template('register.html', form=form, exist=True, repeat=False)
                

    return render_template('register.html', form=form, exist=False, repeat=False)

@auth.route('/reset', methods=['GET', 'POST'])
def reset():
    form=ResetForm()
    if request.method=="POST":
        if form.validate():
            email=form.email.data
            password=form.password.data
            passwordRepeat=form.passwordRepeat.data

            if not password == passwordRepeat:
                return render_template('reset.html', form=form, exist=False, repeat=True)

            account = accountdb.findUser(email)
            if not account:
                return render_template('reset.html', form=form, exist=True, repeat=False)
            else:
                accountdb.reset(email, password)
                return redirect(url_for('main'))

    return render_template('reset.html', form=form, exist=False, repeat=False)



