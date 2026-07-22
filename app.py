from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config
from sqlalchemy import or_

app = Flask(__name__,
            template_folder=os.path.join(Config.BASE_DIR, 'templates'),
            static_folder=os.path.join(Config.BASE_DIR, 'static'))
app.config.from_object(Config)

db = SQLAlchemy(app)

# ================= MODELS ================= #

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    role = db.Column(db.String(20), default='user') # 'admin' or 'user'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"

# Auto-create database tables on startup if they don't exist
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin_pass = generate_password_hash('admin123', method='pbkdf2:sha256')
        db.session.add(User(
            username='admin',
            email='admin@gmail.com',
            password=admin_pass,
            role='admin',
            contact='N/A',
            address='N/A'
        ))
        db.session.commit()

# ================= MIDDLEWARE / UTILS ================= #

def is_logged_in():
    return 'user_id' in session

def is_admin():
    if is_logged_in():
        user = User.query.get(session['user_id'])
        return user and user.role == 'admin'
    return False

def get_current_user():
    if is_logged_in():
        return User.query.get(session['user_id'])
    return None

@app.context_processor
def inject_user():
    return dict(current_user=get_current_user(), is_admin=is_admin())

# ================= ROUTES ================= #

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if is_logged_in():
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        contact = request.form.get('contact')
        address = request.form.get('address')

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('register'))

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or Email already exists.", "error")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            contact=contact,
            address=address,
            role='user'
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful. Please login.", "success")
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        login_id = request.form.get('login_id') # can be username or email
        password = request.form.get('password')
        
        user = User.query.filter((User.username == login_id) | (User.email == login_id)).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("Logged in successfully.", "success")
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials.", "error")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    user = get_current_user()
    if user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
        
    return render_template('dashboard.html', user=user)

@app.route('/profile')
def profile():
    if not is_logged_in():
        return redirect(url_for('login'))
    user = get_current_user()
    return render_template('profile.html', user=user)

@app.route('/profile/update', methods=['POST'])
def profile_update():
    if not is_logged_in():
        return redirect(url_for('login'))
        
    user = get_current_user()
    user.contact = request.form.get('contact')
    user.address = request.form.get('address')
    # Prevent changing email/username directly to avoid unique constraint issues without proper validation logic here
    # If we want to allow email/username change, we must validate uniqueness
    new_username = request.form.get('username')
    new_email = request.form.get('email')

    if new_username != user.username:
        if User.query.filter_by(username=new_username).first():
            flash("Username already taken.", "error")
            return redirect(url_for('profile'))
        user.username = new_username
        
    if new_email != user.email:
        if User.query.filter_by(email=new_email).first():
            flash("Email already registered.", "error")
            return redirect(url_for('profile'))
        user.email = new_email

    db.session.commit()
    flash("Profile updated successfully.", "success")
    return redirect(url_for('dashboard'))

@app.route('/profile/delete', methods=['POST'])
def profile_delete():
    if not is_logged_in():
        return redirect(url_for('login'))
        
    user = get_current_user()
    db.session.delete(user)
    db.session.commit()
    session.pop('user_id', None)
    flash("Your account has been deleted.", "success")
    return redirect(url_for('index'))

# ================= ADMIN ROUTES ================= #

@app.route('/admin')
def admin_dashboard():
    if not is_admin():
        abort(403)
        
    users = User.query.all()
    total_users = len(users)
    admin_count = sum(1 for u in users if u.role == 'admin')
    regular_count = total_users - admin_count
    # Simple logic for "new users" - let's say created in last 7 days, but for simplicity we show total for now
    new_users_count = total_users 
    
    return render_template('admin_dashboard.html', 
                           users=users, 
                           total_users=total_users, 
                           admin_count=admin_count, 
                           regular_count=regular_count,
                           new_users=new_users_count)

@app.route('/admin/add', methods=['POST'])
def admin_add():
    if not is_admin():
        abort(403)
        
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    contact = request.form.get('contact')
    address = request.form.get('address')
    role = request.form.get('role', 'user')

    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        flash("Username or Email already exists.", "error")
        return redirect(url_for('admin_dashboard'))

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        contact=contact,
        address=address,
        role=role
    )
    db.session.add(new_user)
    db.session.commit()
    flash(f"User {username} created successfully.", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
def admin_edit(id):
    if not is_admin():
        abort(403)
        
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.contact = request.form.get('contact')
        user.address = request.form.get('address')
        user.role = request.form.get('role')
        
        new_password = request.form.get('password')
        if new_password:
            user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
            
        try:
            db.session.commit()
            flash(f"User {user.username} updated.", "success")
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash("Error updating user. Email or Username might already exist.", "error")
            
    return render_template('edit_user.html', user=user)

@app.route('/admin/delete/<int:id>', methods=['POST'])
def admin_delete(id):
    if not is_admin():
        abort(403)
        
    user = User.query.get_or_404(id)
    if user.id == session.get('user_id'):
        flash("You cannot delete your own admin account from here.", "error")
        return redirect(url_for('admin_dashboard'))
        
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.username} deleted.", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/search')
def admin_search():
    if not is_admin():
        abort(403)
        
    query = request.args.get('q', '')
    users = User.query.filter(
        or_(
            User.username.ilike(f'%{query}%'),
            User.email.ilike(f'%{query}%'),
            User.role.ilike(f'%{query}%')
        )
    ).all()
    
    total_users = len(User.query.all())
    admin_count = sum(1 for u in User.query.all() if u.role == 'admin')
    regular_count = total_users - admin_count
    
    return render_template('admin_dashboard.html', 
                           users=users, 
                           total_users=total_users, 
                           admin_count=admin_count, 
                           regular_count=regular_count,
                           new_users=total_users,
                           search_query=query)

# ================= ERROR HANDLERS ================= #

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
