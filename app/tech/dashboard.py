from flask import Blueprint, render_template
from flask_login import login_required

tech = Blueprint('tech', __name__)


@tech.route('/dashboard')
@login_required
def dashboard():
    # Later to retrieve actual assigned tasks
    return render_template('tech_dashboard.html')