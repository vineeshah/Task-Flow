from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class AddTaskForm(FlaskForm):
    task = StringField('Task Name', validators=[DataRequired(), Length(min=2, max=50)])
    taskdes = StringField('Task Description', validators=[DataRequired(), Length(min=2, max=50)])
    deadline = DateTimeField("Deadline", format="%H:%M", validators=[DataRequired()])
    submit = SubmitField("Add Task")