from flask import Blueprint, jsonify, request
from controllers.devices_controller import DevicesController
from utils.utils import default_query_ip

devices_router = Blueprint("devices", __name__)


@devices_router.route("/devices")
def get_products():
    result = DevicesController.get()
    return jsonify(result)


@devices_router.route("/devices", methods=["POST"])
def insert_products():
    data = request.get_json()
    ip_address = data.get("ip", default_query_ip)
    print(ip_address)
    result = DevicesController.create(ip_address)
    return jsonify(result)
