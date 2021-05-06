from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# using https://www.youtube.com/watch?v=Z1RJmh_OqeA  tutorial

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # recommendation by Stack Overflow
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# 3 slashes is Relative, and 4 is absolute-path
db = SQLAlchemy(app)  # init db from app settings


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    # nullable = able to be blank
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
        # each time a task is made, return Task and ID of Task


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # creates Task from input of 'content' from Index.html
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            # add new_task to db, commit and then return to Index pg
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "there was an error while adding your Task"

    else:
        # returns all entries ordered by Date Created. So we send tasks >> template in return-line
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
# use unique ID to target Task to delete
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that Task"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "there was an error updating Task"

    else:
        return render_template('update.html', task=task_to_update)


if __name__ == "__main__":
    app.run(debug=True)
