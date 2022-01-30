from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.message import Message
import re

bcrypt = Bcrypt(app)

@app.route('/post/message', methods=['POST'])
def post_message():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Message.is_valid(request.form):
        return redirect('/wall')
    data = {
        "sender_id": request.form['sender_id'],
        "recipient_id": request.form['recipient_id'],
        "message_content": request.form['message_content'],
        "sender": request.form['sender'],
        "recipient": request.form['recipient']
    }
    Message.save(data)
    return redirect(request.referrer)

@app.route('/destroy/message/<int:id>')
def destroy_message(id):
    data = {
        "id": id
    }
    Message.destroy(data)
    return redirect(request.referrer)