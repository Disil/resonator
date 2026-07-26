from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import re
from models import db, User, Note, Tag
from sqlalchemy import or_

def init_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

app = init_app()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def parse_tags(raw_tags):
    if not raw_tags:
        return []

    tags = []
    seen = set()
    for part in re.split(r'[,\n]', raw_tags):
        tag = part.strip().lstrip('#').lower()
        if tag and tag not in seen:
            seen.add(tag)
            tags.append(tag)

    return tags


def sync_note_tags(note, raw_tags):
    tag_names = parse_tags(raw_tags)
    note.tags = []

    for tag_name in tag_names:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.session.add(tag)
        note.tags.append(tag)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return "Username already exists"
        if User.query.filter_by(email=email).first():
            return "Email already exists"

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username']
        password = request.form['password']
        user = User.query.filter(or_(User.username == username_or_email, User.email == username_or_email)).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))

        return "Invalid username/email or password"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.clear()
    return redirect(url_for('login'))

# Dashboard - shows the list of notes
@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    query = request.args.get('q', '').strip()
    selected_tag = request.args.get('tag', '').strip().lower()

    notes_query = Note.query.filter_by(user_id=user.id)
    if query:
        search_term = f'%{query}%'
        notes_query = notes_query.filter(
            or_(
                Note.title.ilike(search_term),
                Note.content.ilike(search_term)
            )
        )

    if selected_tag:
        notes_query = notes_query.join(Note.tags).filter(Tag.name == selected_tag)

    notes = notes_query.distinct().order_by(Note.updated_at.desc()).all()
    return render_template('dashboard.html', user=user, notes=notes, query=query, selected_tag=selected_tag)

# Create note
@app.route('/note/create', methods=['GET', 'POST'])
@login_required
def create_note():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        tags = request.form.get('tags', '')

        if not title or not content:
            return "Title and content are required", 400

        new_note = Note(user_id=session['user_id'], title=title, content=content)
        db.session.add(new_note)
        sync_note_tags(new_note, tags)
        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template('edit_note.html', note=None, tags_value='')

# Edit note
@app.route('/note/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)

    # Check if user is the owner of this note
    if note.user_id != session['user_id']:
        return "Unauthorized", 403

    if request.method == 'POST':
        note.title = request.form.get('title')
        note.content = request.form.get('content')
        tags = request.form.get('tags', '')

        if not note.title or not note.content:
            return "Title and content are required", 400

        sync_note_tags(note, tags)
        db.session.commit()
        return redirect(url_for('dashboard'))

    tags_value = ', '.join(tag.name for tag in note.tags)
    return render_template('edit_note.html', note=note, tags_value=tags_value)

# Delete note
@app.route('/note/<int:note_id>/delete', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)

    # Check if user is the owner of this note
    if note.user_id != session['user_id']:
        return "Unauthorized", 403

    db.session.delete(note)
    db.session.commit()

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)