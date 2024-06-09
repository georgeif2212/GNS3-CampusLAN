from flask import Blueprint, jsonify, request
from controllers.cdp_controller import CdpController
from utils.utils import endpoint_cdp

cdp_router = Blueprint("cdp", __name__)


@cdp_router.route("")
def get_cdp():
    result = CdpController.get()
    return jsonify(result)


@cdp_router.route("", methods=["POST"])
def insert_cdp():
    data = request.get_json()
    result = CdpController.create(data, endpoint_cdp)
    return jsonify(result)
