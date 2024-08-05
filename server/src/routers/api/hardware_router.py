from flask import Blueprint, jsonify, request
from controllers.hardware_controller import HardwareController
from utils.utils import endpoint_hardware

hardware_router = Blueprint("hardware", __name__)

@hardware_router.route("")
def get_hardware():
    result = HardwareController.get()
    return jsonify(result)


@hardware_router.route("", methods=["POST"])
def insert_hardware():
    data = request.get_json()
    result = HardwareController.create(data, endpoint_hardware)
    return jsonify(result)
