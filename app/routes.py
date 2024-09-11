from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Task, User
from app import db
from flask import current_app as app

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return redirect(url_for('login'))

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Usuário já existe')
            return redirect(url_for('register'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuário criado com sucesso!')
        return redirect(url_for('login'))

    return render_template('register.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login bem-sucedido!')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha inválidos.')

    return render_template('login.html')

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta!')
    return redirect(url_for('login'))


@routes.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks)

@routes.route('/task/new', methods=['GET', 'POST'])
@login_required
def create_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        status = request.form.get('status')

        new_task = Task(title=title, description=description, status=status, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        flash('Tarefa criada com sucesso!')
        return redirect(url_for('dashboard'))

    return render_template('create_task.html')

@routes.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.status = request.form.get('status')
        db.session.commit()
        flash('Tarefa atualizada com sucesso!')
        return redirect(url_for('dashboard'))

    return render_template('edit_task.html', task=task)

@routes.route('/task/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Tarefa excluída com sucesso!')
    return redirect(url_for('dashboard'))

