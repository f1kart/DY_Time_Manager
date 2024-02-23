from app import create_app
from app.database import db
from app.models import Truck, Task

app = create_app()
app.app_context().push()  # This pushes an application context manually
