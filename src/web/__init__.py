from flask import Flask
from flask_login import LoginManager
from ..BudgetEngine import User

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hashkadash'
    from .views import views
    from .auth import auth
    from .admin import admin

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.objects.get(id=user_id)

    return app
