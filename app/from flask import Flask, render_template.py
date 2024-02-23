from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from datetime import datetime
from sqlalchemy import orm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
manager = Manager(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)

class Truck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='IN_PROGRESS')  # Add status field
    time_entries = orm.relationship('TimeEntry', backref='task', lazy=True)

class TimeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Interval)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

    def __repr__(self):
        return f'<TimeEntry {self.id}>'

    def start(self):
        self.start_time = datetime.utcnow()

    def stop(self):
        self.end_time = datetime.utcnow()
        self.duration = self.end_time - self.start_time
        self.task.status = 'COMPLETE'
        db.session.commit()

# Routes
@app.route('/task/<int:task_id>/start', methods=['POST'])
def start_task(task_id):
    task = Task.query.get(task_id)
    if task:
        time_entry = TimeEntry(task=task, start_time=datetime.now())
        db.session.add(time_entry)
        db.session.commit()
        return 'Task started successfully'
    else:
        return 'Task not found', 404

@app.route('/task/<int:task_id>/stop', methods=['POST'])
def stop_timer(task_id):
    time_entry = TimeEntry.query.filter_by(task_id=task_id).order_by(TimeEntry.start_time.desc()).first()

    if time_entry:
        time_entry.end_time = datetime.now()
        time_entry.duration = time_entry.end_time - time_entry.start_time
        task = time_entry.task
        if task.status == 'IN_PROGRESS':
            task.status = 'COMPLETE'
        db.session.commit()
        return 'Task stopped successfully'
    else:
        return 'Time entry not found', 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Implement login functionality
    pass

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Implement user registration functionality
    pass

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run()