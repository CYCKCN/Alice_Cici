import flask
from flask import session, request, redirect, render_template, url_for
from flask_user import login_required, UserManager, UserMixin
from app import app

@app.route("/")
def main():
    return render_template('admin_logout.html')




