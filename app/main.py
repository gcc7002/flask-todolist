from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    tags = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Task {self.title}>'

@app.route('/')
def index():
    tasks = Tasks.query.all()
    return render_template('iaindex.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    tags = request.form.get('tags')
    
    if title:
        new_task = Tasks(title=title, description=description, tags=tags)
        db.session.add(new_task)
        db.session.commit()
    
    return redirect('/')

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Tasks.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    task = Tasks.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    if request.method == 'POST':
        task.completed = task.completed
        db.session.commit()
        return redirect('/')
    return redirect('/')

@app.route('/edit/<int:task_id>', methods= ['GET', 'POST'])
def edit_task(task_id):
    task = Tasks.query.get_or_404(task_id)
    pass
    



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5120, host='0.0.0.0')