from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login_page.html')

@app.route('/register', methods = ['POST'])
def register():
    if not User.is_valid(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    session['user_first_name'] = id
    return redirect('/wall')

@app.route('/login', methods = ['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email/Password. Check your spelling.", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/Password. Check your spelling.", "login")
        return redirect('/')
    session['user_id'] = user.id
    session['user_first_name'] = user.first_name
    return redirect('/wall')

@app.route('/wall')
def wall():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    users = User.get_all()
    messages = Message.get_user_messages(data)
    messages_sent = Message.get_messages_sent(data)
    return render_template("wall.html", user = user, users = users, messages = messages, messages_sent = messages_sent)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/testip')
def ip():
    ip_add = request.remote_addr
    return '<h1> Your IP address is:' + ip_add