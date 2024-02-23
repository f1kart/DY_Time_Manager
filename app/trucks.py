from app import db
from app.models import Truck

def get_all_trucks():
    trucks = Truck.query.all()
    return trucks