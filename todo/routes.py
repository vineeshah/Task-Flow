from flask import render_template, url_for, flash, redirect, request
from todo import app, db
from todo.forms import AddTaskForm
from datetime import datetime, time
from todo.models import Tasks
from sqlalchemy import func



# tasks = [
#     {"task_name": "laundry", "deadline": "2025-03-10 08:00"},
#     {"task_name": "cook", "deadline": "2025-03-11 18:00"}
# ]


@app.route("/")
@app.route("/home")
def home():
    current_time = datetime.now().time()
    tasks = Tasks.query.all()
    missed_tasks = Tasks.query.filter(func.TIME(Tasks.deadline) < current_time).all()
    return render_template('home.html', tasks = tasks, missed_tasks=missed_tasks, current_time = current_time.strftime("%H:%M"))

@app.route("/add", methods = ["POST", "GET"])
@app.route("/update/<int:task_id>", methods = ["GET", "POST"])
def add_task(task_id = None):
    form = AddTaskForm()
    update = None

    if task_id:
        update = Tasks.query.get_or_404(task_id)
        if request.method == "GET":
            form.task.data = update.task_name
            form.deadline.data = update.deadline
            form.taskdes.data = update.task_desc

    if form.validate_on_submit():
        if update:
            update.task_name = form.task.data
            update.deadline = form.deadline.data
            update.task_desc = form.taskdes.data
            db.session.commit()
            flash("Task updated succesfully!!")
        else:
            name = form.task.data
            deadline = form.deadline.data
            desc = form.taskdes.data
            existing_task = Tasks.query.filter_by(task_name=name).first()
            if existing_task:
                form.task.errors.append("This task already exists.")
                flash("Something went wrong")
                return render_template("add_task.html", form=form, title="Add new task", task_id = task_id)
            # if deadline <= datetime.now():
            #     form.deadline.errors.append("Deadline must be in the future.")
            #     flash("Something went wrong")
            #     return render_template("add_task.html", form=form, title="Add new task")
            
            new_task = Tasks(task_name = name, task_desc = desc, deadline = deadline)
            db.session.add(new_task)
            db.session.commit()
            flash("Task added succesfully!!")

        
        return redirect("/home")
    return render_template('add_task.html', title = "Add or update task", form = form, task_id = task_id)

@app.route("/delete/<int:task_id>", methods = ["POST"])
def delete(task_id):
    task = Tasks.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("task deleted")
    return redirect("/")