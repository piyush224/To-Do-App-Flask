from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User,db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Logged in successfully!!!", category='success')
                return redirect(url_for('views.home'))
            else:
                flash("password is incorrect", category='error')
        else:
            flash("Email doesn't exist", category='error')

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get('firstName')
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash("User already exist!!", category='error')
        elif len(email) < 4:
            flash("Email is not in correct form", category="error")
        elif len(firstName) < 2:
            flash("First name should be greater than 1 charactor", category="error")
        elif password1 != password2:
            flash("Password is not matching", category="error")
        elif len(password1) < 7:
            flash("password length must be greater than 6", category="error")
        else:
            new_user= User(email=email,firstName=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Account created", category="success")
            return redirect(url_for('views.home'))
    return render_template("sign_up.html",user=current_user)