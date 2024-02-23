from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgresql:kamber33@localhost/dytime'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Truck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Truck('{self.name}', '{self.user}')"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    truck_id = db.Column(db.Integer, db.ForeignKey('truck.id'), nullable=False)
    total_time = db.Column(db.Float)

    def __repr__(self):
        return f"Task('{self.name}', '{self.truck}')"

class TimeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Float)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    def __repr__(self):
        return f"TimeEntry('{self.start_time}')"

@app.route('/task/<int:task_id>/start', methods=['POST'])
def start_timer(task_id):
    truck = Truck.query.get_or_404(truck_id)
    task_to_start = Task.query.filter_by(id=task_id).first_or_404()
    time_entry = TimeEntry(start_time=datetime.now(), task_id=task_id)
    db.session.add(time_entry)
    task = time_entry.task
    task.status = TaskStatus.IN_PROGRESS
    db.session.commit()
    return redirect(f'/truck_details/{truck.id}')

@app.route('/task/<int:task_id>/stop', methods=['POST'])
def stop_timer(task_id):
    time_entry = TimeEntry.query.filter_by(task_id=task_id).order_by(TimeEntry.start_time.desc()).first()
    if time_entry:
        time_entry.end_time = datetime.now()
        time_entry.duration = time_entry.end_time - time_entry.start_time
        task = time_entry.task
        task.status = TaskStatus.COMPLETE
        db.session.commit()
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', tasks=Task.query.all(), trucks=Truck.query.all())

def create_tables():
    db.create_all()


