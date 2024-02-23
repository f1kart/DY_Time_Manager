from flask import Blueprint, render_template

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')
