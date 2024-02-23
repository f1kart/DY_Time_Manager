from app import db
from app.models import Task

def get_tasks_for_truck(truck_id):
    tasks = Task.query.filter_by(truck_id=truck_id).all()
    return tasks
from datetime import datetime, timedelta

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    stop_time = db.Column(db.DateTime)
    truck_id = db.Column(db.Integer, db.ForeignKey('truck.id'), nullable=False)
    paused_time = db.Column(db.DateTime)  # Time when the task was paused
    resume_time = db.Column(db.DateTime)  # Time when the task was resumed

    def total_active_time(self):
        if not self.stop_time:
            now = datetime.utcnow()
            if self.paused_time and not self.resume_time:
                return self.paused_time - self.start_time
            elif self.resume_time:
                return (self.resume_time - self.start_time) + (now - self.resume_time)
            else:
                return now - self.start_time
        else:
            if self.paused_time and not self.resume_time:
                return self.paused_time - self.start_time
            elif self.resume_time:
                return (self.resume_time - self.start_time) + (self.stop_time - self.resume_time)
            else:
                return self.stop_time - self.start_time
