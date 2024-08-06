from flask import Blueprint, jsonify, request
from controllers.software_controller import SoftwareController
from utils.utils import endpoint_hardware

software_router = Blueprint("software", __name__)

@software_router.route("")
def get_software():
    result = SoftwareController.get()
    return jsonify(result)


@software_router.route("", methods=["POST"])
def insert_software():
    data = request.get_json()
    result = SoftwareController.create(data, endpoint_hardware)
    return jsonify(result)
