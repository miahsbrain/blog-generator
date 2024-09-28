from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user
from project.utils.auth import authenticate, create_user

app = Blueprint('app', __name__, template_folder='templates', static_folder='static', static_url_path='/')

@app.route('/')
def index():
    return render_template('app/index.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('app.index'))
        return render_template('app/signin.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user, error = authenticate(email=email, password=password)
        flash(error)
        if user is not None:
            login_user(user=user)
            return redirect(url_for('app.index'))
        return render_template('app/signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('app/signup.html')
    elif request.method == 'POST':
        first_name = request.form.get('fname')
        last_name = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('cpassword')

        user, error = create_user(first_name=first_name, last_name=last_name, email=email, password=password, confirm_password=confirm_password)
        flash(error)
        if user is not None:
            login_user(user=user)
            return redirect(url_for('app.index'))

        return render_template('app/signup.html')