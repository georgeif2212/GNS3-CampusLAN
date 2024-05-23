from flask import Blueprint, jsonify, request
from controllers.interfaces_controller import InterfacesController
from utils.utils import default_query_ip, endpoint_native

interfaces_router = Blueprint("interfaces", __name__)


@interfaces_router.route("/interfaces")
def get_interfaces():
    pass

@interfaces_router.route("/interfaces", methods=["POST"])
def insert_interfaces():
    pass