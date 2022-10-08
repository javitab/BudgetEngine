from flask import Flask
from flask_login import LoginManager
from ..BudgetEngine.user import User

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hashkadash'
    from .views import views
    from .auth import auth
    from .admin import admin
    from .proj import proj
    from .tx import tx
    from .acct import acct
    from .exps import exps
    from .revs import revs
    from .projs import projs

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(proj, url_prefix='/projection')
    app.register_blueprint(tx, url_prefix='/tx')
    app.register_blueprint(acct, url_prefix='/accts')
    app.register_blueprint(exps, url_prefix='/exps')
    app.register_blueprint(revs, url_prefix='/revs')
    app.register_blueprint(projs, url_prefix='/projs')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.objects.get(id=user_id)

    return app
