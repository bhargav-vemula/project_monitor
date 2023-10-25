from flask import Response, jsonify

"""
proper error responses are mentioned and saved here

"""


def mongo_error() -> Response:
    output = {"msg": "401 error: mongodb is down."}
    resp = jsonify({'result': output})
    resp.status_code = 401
    return resp


def sql_server() -> Response:
    output = {"error":
                  {"msg": "data is not available in bigdata."}
              }
    resp = jsonify({'result': output})
    resp.status_code = 401
    return resp


def server_down() -> Response:
    output = {"error":
                  {"msg": "403 error: server is down."}
              }
    resp = jsonify({'result': output})
    resp.status_code = 403
    return resp




def status() -> Response:
    output = {"error":
                  {"msg": "403 error"}
              }
    resp = jsonify({'result': output})
    resp.status_code = 403
    return resp


def status_sucess() -> Response:
    output = {"error":
                  {"msg": "working fine"}
              }
    resp = jsonify({'result': output})
    resp.status_code = 200
    return resp


