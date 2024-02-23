from flask import Blueprint, render_template

tech_blueprint = Blueprint('tech', __name__)

@tech_blueprint.route('/tasks')
def tasks():
    return render_template('tech/tasks.html')
