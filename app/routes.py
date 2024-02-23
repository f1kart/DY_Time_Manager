from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
# from .models import User  # Ensure you have a User model defined
from .database import db

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # Login logic here
    return render_template('auth/login.html')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # Registration logic here
    return render_template('auth/register.html')
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/users/<int:id>', methods=['PUT'])
@role_required('admin')
def update_user(id):
    user = User.query.get_or_404(id)
    user.username = request.json.get('username', user.username)
    db.session.commit()
    return jsonify(user.to_dict())

@app.route('/users', methods=['POST'])
@role_required('admin')
def create_user():
    user = User(username=request.json['username'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@app.route('/users/<int:id>', methods=['DELETE'])
@role_required('admin')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'result': True})
