import flask
def handle_custom_error(error):
    response = {
        "status": "error",
        "message": error.message,
        "name": error.name,
        "cause": error.cause
    }
    return flask.jsonify(response), error.code

def handle_404_error(error):
    response = {
        "status": "error",
        "message": "Resource not found"
    }
    return flask.jsonify(response), 404


def handle_500_error(error):
    response = {
        "status": "error",
        "message": "Internal server error"
    }
    return flask.jsonify(response), 500