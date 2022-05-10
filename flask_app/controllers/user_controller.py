from crypt import methods
from pprint import pprint
from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def save_user():
    if not User.validate_user(request.form):
        return redirect('/')
    data ={
        "first_name":request.form['first_name'],
        "last_name":request.form['last_name'],
        "birthdate":request.form['birthdate'],
        "email":request.form['email'],
        "password":bcrypt.generate_password_hash(request.form['password'])
    }
    id =User.save(data)
    session['user_id'] = id
    return redirect('/success')


@app.route('/login', methods = ['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/success')

@app.route('/success')
def welcome():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    user = User.get_one(data)
    messages = Message.get_user_messages(data)
    users = User.get_all()
    return render_template('welcome.html', user = user, users = users, messages = messages)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



