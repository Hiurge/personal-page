from flask import Flask
from flask_login import LoginManager

import datetime
import os

from db_x import CommentsTable, MappingTable_UserPostComment, PortfolioPageDB
from user_system.user_system.db import UsersTable



# Create tables.
access = {'dbname':'lp_portfolio_articles', 'dbuser':'luke'}
for table in [PortfolioPageDB(access) UsersTable(access), CommentsTable(access), MappingTable_UserPostComment(access)]:
    table.create_table()

login_manager = LoginManager()



def create_app():

    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object('config.Config')

    login_manager.init_app(app)
    with app.app_context():
        from .user_system import user_system_routes
        from .content_system import content_system_routes
        app.register_blueprint(user_system_routes.user_system_bp)
        app.register_blueprint(content_system_routes.content_system_bp)

        return app