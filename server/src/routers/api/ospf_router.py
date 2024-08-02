from flask import Blueprint, jsonify, request
from controllers.ospf_controller import OSPFController 
from utils.utils import default_query_ip, endpoint_native

ospf_router = Blueprint("ospf", __name__)


@ospf_router.route("")
def get_ospf():
    result = OSPFController.get()
    return jsonify(result)


@ospf_router.route("", methods=["POST"])
def insert_ospf():
    data = request.get_json()
    result = OSPFController.create(data, endpoint_native)
    return jsonify(result)
