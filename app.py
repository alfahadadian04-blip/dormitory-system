from flask import Flask
from config import Config
from models import db, User
from flask_login import LoginManager
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    with app.app_context():
        db.create_all()
        # Create admin user if doesn't exist
        admin = User.query.filter_by(username=Config.ADMIN_USERNAME).first()
        if not admin:
            from werkzeug.security import generate_password_hash
            admin = User(
                username=Config.ADMIN_USERNAME,
                password=generate_password_hash(Config.ADMIN_PASSWORD)
            )
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user '{Config.ADMIN_USERNAME}' created")
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=Config.FLASK_DEBUG)
