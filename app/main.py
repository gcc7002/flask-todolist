from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'iHatemyself'

db = SQLAlchemy(app)

#creating the database model
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    tags = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Task {self.title}>'
    
    #creating the form for edit tasks
class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    tags = StringField('Tags')
    completed = BooleanField('Completed')
    submit = SubmitField('Submit')

@app.route('/')
def index():
    tasks = Tasks.query.all()
    forms = {task.id: TaskForm(obj=task) for task in tasks}
    return render_template('home.html', tasks=tasks, forms=forms)

#basic CRUD operations
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

@app.route('/edit/<int:task_id>', methods= ['POST'])
def edit_task(task_id):
    task = Tasks.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        form.populate_obj(task)
        db.session.commit()
    return render_template('home.html', task=task, form=form)
    



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=5120, host='0.0.0.0')