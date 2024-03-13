from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class NoteEditForm(FlaskForm):
    content = TextAreaField('Note Content', validators=[DataRequired()])
    submit = SubmitField('Update Note')


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


from wtforms import StringField, DateTimeField, SelectField, SubmitField
from wtforms.validators import DataRequired


class AddTaskForm(FlaskForm):
    """Form for adding a new task."""

    task_name = StringField('Task Name', validators=[DataRequired()])
    start_time = DateTimeField('Start Time', validators=[DataRequired()])
    stop_time = DateTimeField('Stop Time', validators=[DataRequired()])
    truck = SelectField('Truck', choices=[(truck.id, truck.truck_id) for truck in Truck.query.all()], validators=[DataRequired()])
    submit = SubmitField('Add Task')

# app/forms.py

class RestoreForm(FlaskForm):
    destination_folder_id = IntegerField('Destination Folder ID', validators=[DataRequired()])
    submit = SubmitField('Restore')
