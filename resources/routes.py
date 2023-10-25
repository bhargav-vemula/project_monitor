from flask_restful import Api

from project_monitor.projects.view import PortalMonitoring,PortalDetails

def initialize_routes(app):
    api = Api(app)
    #user management path
    api.add_resource(PortalMonitoring, '/project_monitor/view')
    api.add_resource(PortalDetails, '/project_monitor/details')
