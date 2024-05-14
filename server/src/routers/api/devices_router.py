from flask import Blueprint, jsonify
from controllers.devices_controller import DevicesController

devices_router = Blueprint("devices", __name__)


@devices_router.route("/devices")
def get_products():
    result = DevicesController.get()
    return jsonify(result)
