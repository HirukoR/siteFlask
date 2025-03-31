from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from app.config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    
    # Убедимся, что директория instance существует
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Добавляем функцию now в контекст всех шаблонов
    @app.context_processor
    def inject_now():
        return {'now': datetime.now}
    
    from app.routes.auth import auth
    from app.routes.admin import admin
    from app.routes.waiter import waiter
    from app.routes.cook import cook
    from app.routes.main import main
    
    app.register_blueprint(auth)
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(waiter, url_prefix='/waiter')
    app.register_blueprint(cook, url_prefix='/cook')
    app.register_blueprint(main)
    
    return app 