from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db
from app import app, db
from flask import request, jsonify
from app.models import Truck, Task
from datetime import datetime
from flask import request, jsonify
from . import app, db
from .models import Task
from flask_login import login_required
from flask_login import current_user

return render_template('index.html', current_user=current_user)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/task', methods=['POST'])
def add_task():
    task_data = request.json
    new_task = Task(name=task_data['name'], description=task_data['description'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added"}), 201

@app.route('/trucks', methods=['GET', 'POST'])
def handle_trucks():
    if request.method == 'POST':
        data = request.get_json()
        new_truck = Truck(make=data['make'], model=data['model'], year=data['year'])
        db.session.add(new_truck)
        db.session.commit()
        return jsonify(new_truck), 201
    else:  # GET
        trucks = Truck.query.all()
        return jsonify([truck.to_dict() for truck in trucks]), 200

@app.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'POST':
        data = request.get_json()
        new_task = Task(name=data['name'], description=data['description'], truck_id=data['truck_id'])
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.to_dict()), 201
    else:  # GET
        tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks]), 200

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

# app/routes.py

from flask import jsonify
from ..models import Truck

# Route to get all trucks
@app.route('/trucks', methods=['GET'])
@login_required
def get_trucks():
    trucks = Truck.query.all()
    return jsonify([truck.to_dict() for truck in trucks])

# Route to get all files of a truck
@app.route('/truck/<int:truck_id>/files', methods=['GET'])
@login_required
def get_truck_files(truck_id):
    truck = Truck.query.get_or_404(truck_id)
    files = truck.files.all()
    return jsonify([file.to_dict() for file in files])

# routes.py

@app.route('/trucks', methods=['GET'])
@login_required
def get_trucks():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    trucks = Truck.query.paginate(page, per_page, False).items
    return jsonify([truck.to_dict() for truck in trucks])

# routes.py

@app.route('/trucks', methods=['GET'])
@login_required
def get_trucks():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    trucks = Truck.query.filter(Truck.name.contains(search)).paginate(page, per_page, False).items
    return jsonify([truck.to_dict() for truck in trucks])

# routes.py

from sqlalchemy import desc

@app.route('/trucks', methods=['GET'])
@login_required
def get_trucks():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')
    if order == 'desc':
        sort = desc(sort)
    trucks = Truck.query.filter(Truck.name.contains(search)).order_by(sort).paginate(page, per_page, False).items
    return jsonify([truck.to_dict() for truck in trucks])

# Flask

@app.route('/manage_files/<int:truck_id>')
def manage_files(truck_id):
    # Fetch the truck and its files from the database
    truck = Truck.query.get(truck_id)
    files = File.query.filter_by(truck_id=truck_id).all()

    # Render the manage_files template with the truck and its files
    return render_template('manage_files.html', truck=truck, files=files)

# Flask

@app.route('/files/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    # Fetch the file from the database and delete it
    file = File.query.get(file_id)
    db.session.delete(file)
    db.session.commit()
    return jsonify({'message': 'File deleted successfully'})

@app.route('/files/<int:file_id>', methods=['PUT'])
def edit_file(file_id):
    # Fetch the file from the database and update its name
    file = File.query.get(file_id)
    new_name = request.json.get('name')
    file.name = new_name
    db.session.commit()
    return jsonify({'message': 'File updated successfully'})

from flask import send_from_directory

@app.route('/download_file/<int:file_id>')
def download_file(file_id):
    # Fetch the file from the database
    file = File.query.get(file_id)
    
    # Send the file to the client
    return send_from_directory(app.config['UPLOAD_FOLDER'], file.filename)
# app/main/routes.py

from flask import request

@app.route('/search_files', methods=['POST'])
def search_files():
    query = request.form.get('query')
    files = File.query.filter(File.name.contains(query)).all()
    return render_template('main/search_results.html', files=files)

# app/main/routes.py

from .forms import CreateFolderForm
from ..models import Folder

@app.route('/create_folder', methods=['GET', 'POST'])
@login_required
def create_folder():
    form = CreateFolderForm()
    if form.validate_on_submit():
        folder = Folder(name=form.name.data, user_id=current_user.id)
        db.session.add(folder)
        db.session.commit()
        flash('Folder created successfully')
        return redirect(url_for('main.index'))
    return render_template('main/create_folder.html', form=form)

@app.route('/folders')
@login_required
def folders():
    folders = Folder.query.filter_by(user_id=current_user.id).all()
    return render_template('main/folders.html', folders=folders)
# app/main/routes.py

from .forms import UploadFileForm

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    form = UploadFileForm()
    form.folder.choices = [(folder.id, folder.name) for folder in Folder.query.filter_by(user_id=current_user.id).all()]
    if form.validate_on_submit():
        filename = photos.save(form.file.data)
        file = File(name=filename, user_id=current_user.id, folder_id=form.folder.data)
        db.session.add(file)
        db.session.commit()
        flash('File uploaded successfully')
        return redirect(url_for('main.index'))
    return render_template('main/upload_file.html', form=form)
# app/main/routes.py

from .forms import RenameFolderForm

@app.route('/rename_folder/<int:folder_id>', methods=['GET', 'POST'])
@login_required
def rename_folder(folder_id):
    folder = Folder.query.get(folder_id)
    if folder and folder.user_id == current_user.id:
        form = RenameFolderForm()
        if form.validate_on_submit():
            folder.name = form.name.data
            db.session.commit()
            flash('Folder renamed successfully')
            return redirect(url_for('main.folders'))
        return render_template('main/rename_folder.html', form=form)
    else:
        flash('You do not have permission to rename this folder')
        return redirect(url_for('main.folders'))
# app/main/routes.py

from .forms import MoveFileForm

@app.route('/move_file/<int:file_id>', methods=['GET', 'POST'])
@login_required
def move_file(file_id):
    file = File.query.get(file_id)
    if file and file.user_id == current_user.id:
        form = MoveFileForm()
        form.folder.choices = [(folder.id, folder.name) for folder in Folder.query.filter_by(user_id=current_user.id).all()]
        if form.validate_on_submit():
            file.folder_id = form.folder.data
            db.session.commit()
            flash('File moved successfully')
            return redirect(url_for('main.files'))
        return render_template('main/move_file.html', form=form)
    else:
        flash('You do not have permission to move this file')
        return redirect(url_for('main.files'))

# app/main/routes.py

@app.route('/delete_file/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    file = File.query.get(file_id)
    if file and file.user_id == current_user.id:
        db.session.delete(file)
        db.session.commit()
        flash('File deleted successfully')
    else:
        flash('You do not have permission to delete this file')
    return redirect(url_for('main.files'))
# app/main/routes.py

@app.route('/delete_folder/<int:folder_id>', methods=['POST'])
@login_required
def delete_folder(folder_id):
    folder = Folder.query.get(folder_id)
    if folder and folder.user_id == current_user.id:
        db.session.delete(folder)
        db.session.commit()
        flash('Folder deleted successfully')
    else:
        flash('You do not have permission to delete this folder')
    return redirect(url_for('main.folders'))
# app/models.py

class File(db.Model):
    # existing fields...
    deleted = db.Column(db.Boolean, default=False)

class Folder(db.Model):
    # existing fields...
    deleted = db.Column(db.Boolean, default=False)

# app/main/routes.py

@app.route('/delete_file/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    file = File.query.get(file_id)
    if file and file.user_id == current_user.id:
        file.deleted = True
        db.session.commit()
        flash('File moved to trash bin')
    else:
        flash('You do not have permission to delete this file')
    return redirect(url_for('main.files'))

@app.route('/delete_folder/<int:folder_id>', methods=['POST'])
@login_required
def delete_folder(folder_id):
    folder = Folder.query.get(folder_id)
    if folder and folder.user_id == current_user.id:
        folder.deleted = True
        db.session.commit()
        flash('Folder moved to trash bin')
    else:
        flash('You do not have permission to delete this folder')
    return redirect(url_for('main.folders'))

# app/main/routes.py

@app.route('/trash_bin')
@login_required
def trash_bin():
    deleted_files = File.query.filter_by(user_id=current_user.id, deleted=True).all()
    deleted_folders = Folder.query.filter_by(user_id=current_user.id, deleted=True).all()
    return render_template('main/trash_bin.html', deleted_files=deleted_files, deleted_folders=deleted_folders)

# app/main/routes.py

@app.route('/restore_file/<int:file_id>', methods=['POST'])
@login_required
def restore_file(file_id):
    file = File.query.get(file_id)
    if file and file.user_id == current_user.id and file.deleted:
        file.deleted = False
        db.session.commit()
        flash('File restored')
    else:
        flash('You do not have permission to restore this file')
    return redirect(url_for('main.trash_bin'))

@app.route('/restore_folder/<int:folder_id>', methods=['POST'])
@login_required
def restore_folder(folder_id):
    folder = Folder.query.get(folder_id)
    if folder and folder.user_id == current_user.id and folder.deleted:
        folder.deleted = False
        db.session.commit()
        flash('Folder restored')
    else:
        flash('You do not have permission to restore this folder')
    return redirect(url_for('main.trash_bin'))

# app/main/routes.py

@app.route('/permanent_delete_file/<int:file_id>', methods=['POST'])
@login_required
def permanent_delete_file(file_id):
    file = File.query.get(file_id)
    if file and file.user_id == current_user.id and file.deleted:
        db.session.delete(file)
        db.session.commit()
        flash('File permanently deleted')
    else:
        flash('You do not have permission to permanently delete this file')
    return redirect(url_for('main.trash_bin'))

@app.route('/permanent_delete_folder/<int:folder_id>', methods=['POST'])
@login_required
def permanent_delete_folder(folder_id):
    folder = Folder.query.get(folder_id)
    if folder and folder.user_id == current_user.id and folder.deleted:
        db.session.delete(folder)
        db.session.commit()
        flash('Folder permanently deleted')
    else:
        flash('You do not have permission to permanently delete this folder')
    return redirect(url_for('main.trash_bin'))

# app/main/routes.py

@app.route('/empty_trash_bin', methods=['POST'])
@login_required
def empty_trash_bin():
    deleted_files = File.query.filter_by(user_id=current_user.id, deleted=True).all()
    for file in deleted_files:
        db.session.delete(file)
    deleted_folders = Folder.query.filter_by(user_id=current_user.id, deleted=True).all()
    for folder in deleted_folders:
        db.session.delete(folder)
    db.session.commit()
    flash('Trash bin emptied')
    return redirect(url_for('main.trash_bin'))

# app/main/routes.py

from flask import request

@app.route('/trash_bin')
@login_required
def trash_bin():
    sort = request.args.get('sort', 'date')
    filter = request.args.get('filter', 'all')

    if sort == 'name':
        order_by = File.name
    elif sort == 'size':
        order_by = File.size
    else:
        order_by = File.date

    if filter == 'files':
        deleted_files = File.query.filter_by(user_id=current_user.id, deleted=True).order_by(order_by).all()
        deleted_folders = []
    elif filter == 'folders':
        deleted_files = []
        deleted_folders = Folder.query.filter_by(user_id=current_user.id, deleted=True).order_by(order_by).all()
    else:
        deleted_files = File.query.filter_by(user_id=current_user.id, deleted=True).order_by(order_by).all()
        deleted_folders = Folder.query.filter_by(user_id=current_user.id, deleted=True).order_by(order_by).all()

    return render_template('main/trash_bin.html', deleted_files=deleted_files, deleted_folders=deleted_folders)

# app/main/routes.py

@app.route('/trash_bin')
@login_required
def trash_bin():
    # existing code...

    search = request.args.get('search', '')

    if search:
        deleted_files = [file for file in deleted_files if search in file.name]
        deleted_folders = [folder for folder in deleted_folders if search in folder.name]

    return render_template('main/trash_bin.html', deleted_files=deleted_files, deleted_folders=deleted_folders)

# app/main/routes.py

from flask import send_from_directory

@app.route('/preview/<int:file_id>')
@login_required
def preview(file_id):
    file = File.query.get(file_id)
    if file and file.user_id == current_user.id and file.deleted and file.type.startswith('image/'):
        return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], file.filename)
    else:
        flash('You do not have permission to preview this file')
    return redirect(url_for('main.trash_bin'))

# app/main/routes.py

@app.route('/download/<int:file_id>')
@login_required
def download(file_id):
    file = File.query.get(file_id)
    if file and file.user_id == current_user.id and file.deleted:
        return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], file.filename, as_attachment=True)
    else:
        flash('You do not have permission to download this file')
    return redirect(url_for('main.trash_bin'))

# app/main/routes.py

@app.route('/restore_to/<int:item_id>/<item_type>', methods=['GET', 'POST'])
@login_required
def restore_to(item_id, item_type):
    if item_type == 'file':
        item = File.query.get(item_id)
    elif item_type == 'folder':
        item = Folder.query.get(item_id)
    else:
        flash('Invalid item type')
        return redirect(url_for('main.trash_bin'))

    if item and item.user_id == current_user.id and item.deleted:
        form = RestoreForm()
        if form.validate_on_submit():
            destination_folder = Folder.query.get(form.destination_folder_id.data)
            if destination_folder and destination_folder.user_id == current_user.id and not destination_folder.deleted:
                item.folder_id = destination_folder.id
                item.deleted = False
                db.session.commit()
                flash('Item restored to destination folder')
            else:
                flash('Invalid destination folder')
            return redirect(url_for('main.trash_bin'))
        return render_template('main/restore_to.html', form=form)
    else:
        flash('You do not have permission to restore this item')
    return redirect(url_for('main.trash_bin'))

