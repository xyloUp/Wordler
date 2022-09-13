from flask import Flask
from .api import CreateApi
from flask_login import LoginManager

class Start:

    DB_NAME = "accounts.db"

    @classmethod
    def create_app(cls) -> Flask:
        """
        Creats And Configures Flask App Icluding DB, session etc
        """
        app = Flask(__name__)
        app.config["SECRET_KEY"] = "secret"
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{cls.DB_NAME}"

        from .views import views 
        from .auth import auth

        for item in [views, auth]:
            app.register_blueprint(item, url_prefix="/")

        api = CreateApi(app)
        api.add_all()

        from .models import db, Account

        db.init_app(app)
        cls.create_db(db, app)

        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.login_view = "auth.login"

        @login_manager.user_loader
        def load_user(user_id):
            """
            Loads User Using ID
            """
            return Account.query.filter_by(id=user_id).first()

        return app

    @classmethod
    def start_app(cls, debug: bool = True) -> None:
        app = cls.create_app()
        app.run(debug=debug)

    @classmethod
    def create_db(cls, db, app) -> None:
        """
        Creates Sqlite Database If It Desn't Already Exist
        """
        if not __import__("os").path.exists(f"website\\{cls.DB_NAME}"):
            db.create_all(app=app)
            print("CREATED DATABASE")