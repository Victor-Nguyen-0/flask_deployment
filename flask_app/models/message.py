from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
from flask import flash
import math

class Message:
    db = "private_wall_schema"
    def __init__(self, data):
        self.sender_id = data['sender_id']
        self.recipient_id = data['recipient_id']
        self.id = data['id']
        self.message_content = data['message_content']
        self.sender = data['sender']
        self.recipient = data['recipient']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60) / 60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"

    @classmethod
    def save(cls, data):
        query = "INSERT INTO messages (sender_id, recipient_id, message_content, sender, recipient) VALUES (%(sender_id)s, %(recipient_id)s, %(message_content)s, %(sender)s, %(recipient)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_user_messages(cls, data):
        query = "SELECT users.first_name as sender, users2.first_name as recipient, messages.* FROM users LEFT JOIN messages ON users.id = messages.sender_id LEFT JOIN users as users2 ON users2.id = messages.recipient_id WHERE users2.id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        messages = []
        for message in results:
            messages.append(cls(message))
        return messages

    @classmethod
    def get_messages_sent(cls, data):
        query = "SELECT * FROM messages WHERE sender_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        messages = []
        for message in results:
                messages.append(cls(message))
        return messages

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM messages WHERE messages.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def is_valid(message):
        is_valid = True
        if len(message['message_content']) <5:
            is_valid = False
            flash("Message must be at least 5 characters.", "message")
        return is_valid