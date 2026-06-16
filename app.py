from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///german_learning.db'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    progress = db.relationship('Progress', backref='user', lazy=True)

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # 'audio', 'video', 'text', 'image', 'pdf'
    content = db.Column(db.Text)
    file_path = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    progress_items = db.relationship('Progress', backref='lesson', lazy=True)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/darslar')
def lessons():
    lessons = Lesson.query.all()
    return render_template('lessons.html', lessons=lessons)

@app.route('/api/lessons', methods=['GET'])
def get_lessons():
    category = request.args.get('category')
    if category:
        lessons = Lesson.query.filter_by(category=category).all()
    else:
        lessons = Lesson.query.all()
    return jsonify([{'id': l.id, 'title': l.title, 'category': l.category} for l in lessons])

@app.route('/api/lesson/<int:lesson_id>', methods=['GET'])
def get_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    return jsonify({
        'id': lesson.id,
        'title': lesson.title,
        'description': lesson.description,
        'category': lesson.category,
        'content': lesson.content,
        'file_path': lesson.file_path
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
