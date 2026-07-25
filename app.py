from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
from models import db, User, Note

def init_app():
    app = Flask(__name__)
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

@app.route('/')
@login_required
def index():
    user = User.query.get(session['user_id'])
    notes = Note.query.filter_by(user_id=user.id).all()
    return render_template('index.html', user=user, notes=notes)

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

        new_user = User(username=username, email=email, password=password)
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

        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('index'))

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
    notes = Note.query.filter_by(user_id=user.id).all()
    return render_template('dashboard.html', user=user, notes=notes)

if __name__ == '__main__':
    app.run(debug=True)