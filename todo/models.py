from datetime import datetime
from todo import db

class Tasks(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)  
    task_name = db.Column(db.String(50), unique = True, nullable=False)
    task_desc = db.Column(db.String(150), nullable=True, default = "do this ASAP!!")
    deadline = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Task('{self.task_name}','{self.task_desc}', '{self.deadline}')"