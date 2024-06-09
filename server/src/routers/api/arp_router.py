from flask import Blueprint, jsonify, request
from controllers.arp_controller import ArpController
from utils.utils import default_query_ip, endpoint_arp

arp_router = Blueprint("arp", __name__)


@arp_router.route("")
def get_arp():
    result = ArpController.get()
    return jsonify(result)


@arp_router.route("", methods=["POST"])
def insert_arp():
    data = request.get_json()
    result = ArpController.create(data, endpoint_arp)
    return jsonify(result)
