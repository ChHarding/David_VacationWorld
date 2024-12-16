from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.
    This function processes the login form submission. If the request method is POST,
    it retrieves the email and password from the form. It then checks if a user with
    the provided email exists in the database. If the user exists and the password
    matches, the user is logged in and redirected to the main page. If the password
    is incorrect or the email does not exist, appropriate error messages are flashed.
    Returns:
        Response: Renders the main_page with the current user context if login is successful, otherwise render login template.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.main_page'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    """
    Logs out the current user and redirects them to the login page.

    This function calls the `logout_user` function to log out the current user
    and then redirects the user to the login page using the `url_for` function
    with the 'auth.login' endpoint.
    Returns:
        Response: Renders the login template.
    """
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """
    Handle the sign-up process for a new user.
    This function processes the sign-up form submission. It validates the input data,
    checks for existing users with the same email, and creates a new user if all
    validations pass. It also handles user login upon successful account creation.
    Returns:
        Response: A redirect to the main page if the account is created successfully,
                  or the sign-up page with error messages if validation fails.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, last_name=last_name, password=password1)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.main_page'))

    return render_template("sign_up.html", user=current_user)