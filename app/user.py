from flask_sqlalchemy import SQLAlchemy
from app.models import User, Truck, Task

def get_technician_data(user_id):
    user = User.query.get(user_id)  # Retrieve technician by ID
    if user:
        assigned_truck = user.trucks.first()  # Assuming users have assigned trucks
        truck_tasks = Task.query.filter_by(truck_id=assigned_truck.id).all()
        return assigned_truck, truck_tasks 
    else:
        return None, None  # Handle the case where the user isn't found