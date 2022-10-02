from flask import Flask
from flask_login import LoginManager
from BudgetEngine.data import *
from BudgetEngine.user import User

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hashkadash'
    from web.views import views
    from web.auth import auth
    from web.admin import admin

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.objects.get(id=user_id)
        
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)