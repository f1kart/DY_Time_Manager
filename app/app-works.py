from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
# Ensure you have the correct URI for your database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dyconcrete.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class SerializableModel(db.Model):
    __abstract__ = True

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class MyModel(SerializableModel):
    __tablename__ = 'my_model'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

# Corrected Flask route parameters and added missing imports
@app.route('/task/<int:task_id>/start', methods=['POST'])
def start_timer(task_id):
    # Assuming Truck and Task models are defined similarly to MyModel
    task_to_start = Task.query.get(task_id)
    if task_to_start:
        time_entry = TimeEntry(start_time=datetime.now(), task_id=task_id)
        db.session.add(time_entry)
        db.session.commit()
        return jsonify({'message': 'Timer started'}), 200
    return jsonify({'error': 'Task not found'}), 404

@app.route('/task/<int:task_id>/stop', methods=['POST'])
def stop_timer(task_id):
    time_entry = TimeEntry.query.filter_by(task_id=task_id).order_by(TimeEntry.start_time.desc()).first()
    if time_entry:
        time_entry.end_time = datetime.now()
        db.session.commit()
        return jsonify({'message': 'Timer stopped'}), 200
    return jsonify({'error': 'Time entry not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
