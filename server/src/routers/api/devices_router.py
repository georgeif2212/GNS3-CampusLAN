from flask import Blueprint, jsonify, request
from controllers.devices_controller import DevicesController
from utils.utils import default_query_ip, endpoint_native

devices_router = Blueprint("devices", __name__)


@devices_router.route("")
def get_devices():
    result = DevicesController.get()
    return jsonify(result)


@devices_router.route("", methods=["POST"])
def insert_devices():
    data = request.get_json()
    ip_address = data.get("ip", default_query_ip)
    result = DevicesController.create(ip_address, endpoint_native)
    return jsonify(result)
