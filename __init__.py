from flask import Blueprint

pm_app = Blueprint('pm', __name__)

from project_monitor.resources import routes



def init_app(app):
    app.register_blueprint(pm_app)
    from project_monitor.resources.routes import initialize_routes
    initialize_routes(app)
