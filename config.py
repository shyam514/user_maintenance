import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-key-for-portfolio-app'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Handle Vercel serverless read-only filesystem by storing SQLite DB and uploads in /tmp
    if os.environ.get('VERCEL'):
        db_path = '/tmp/users.db'
        upload_path = '/tmp/uploads'
    else:
        db_path = os.path.join(BASE_DIR, 'users.db')
        upload_path = os.path.join(BASE_DIR, 'uploads')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = upload_path
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16 MB limit
