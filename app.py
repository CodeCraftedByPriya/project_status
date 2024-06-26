from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Import models here to avoid circular import issues
from models import Project


@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)


@app.route('/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        progress = request.form['progress']

        new_project = Project(name=name, description=description, progress=progress)
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_project.html')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_project(id):
    project = Project.query.get(id)
    if request.method == 'POST':
        project.name = request.form['name']
        project.description = request.form['description']
        project.progress = request.form['progress']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update_project.html', project=project)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
