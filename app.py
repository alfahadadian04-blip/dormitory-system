from flask import Flask
from config import Config
from models import db, User
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import os
import sys

# Create app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
try:
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
except Exception as e:
    print(f"Error loading blueprints: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()

# Initialize database on first request
@app.before_request
def init_db():
    if not hasattr(app, '_db_initialized'):
        with app.app_context():
            try:
                db.create_all()
                # Create admin user if doesn't exist
                admin = User.query.filter_by(username=Config.ADMIN_USERNAME).first()
                if not admin:
                    admin = User(
                        username=Config.ADMIN_USERNAME,
                        password=generate_password_hash(Config.ADMIN_PASSWORD)
                    )
                    db.session.add(admin)
                    db.session.commit()
                    print(f"Admin user '{Config.ADMIN_USERNAME}' created")
                app._db_initialized = True
            except Exception as e:
                print(f"Database initialization error: {e}", file=sys.stderr)

if __name__ == '__main__':
    app.run(debug=Config.FLASK_DEBUG, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
