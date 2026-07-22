import os
import sys

# Add parent directory to path so we can import app and db
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, User
from werkzeug.security import generate_password_hash

def create_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created.")

        # Check if admin already exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            hashed_password = generate_password_hash('admin123', method='pbkdf2:sha256')
            new_admin = User(
                username='admin',
                email='admin@gmail.com',
                password=hashed_password,
                role='admin',
                contact='N/A',
                address='N/A'
            )
            db.session.add(new_admin)
            db.session.commit()
            print("Default admin user created successfully.")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    create_database()
