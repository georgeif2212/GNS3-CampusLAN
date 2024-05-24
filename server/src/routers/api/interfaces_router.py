from flask import Blueprint, jsonify, request
from controllers.interfaces_controller import InterfacesController
from utils.utils import default_query_ip, endpoint_native

interfaces_router = Blueprint("interfaces", __name__)


@interfaces_router.route("", methods=["GET"])
def get_interfaces():
    result = InterfacesController.get()
    return jsonify(result)


@interfaces_router.route("", methods=["POST"])
def insert_interfaces():
    request_json = request.get_json()
    result = InterfacesController.create(request_json, endpoint_native)
    return jsonify(result)
