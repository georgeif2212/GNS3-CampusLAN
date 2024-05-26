from flask import Blueprint, jsonify, request, render_template, make_response
from controllers.devices_controller import DevicesController
from controllers.interfaces_controller import InterfacesController
from utils.utils import default_query_ip, endpoint_native
import pdfkit

reports_router = Blueprint("reports", __name__)


@reports_router.route("/devices")
def devices_report():
    result = DevicesController.get()

    return render_template("report_base.html", devices=result)


@reports_router.route("/devices/pdf", methods=["GET"])
def devices_report_pdf():
    result = DevicesController.get()

    rendered = render_template("report_base.html", devices=result)
    pdf = pdfkit.from_string(rendered, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=report.pdf"
    return response


@reports_router.route("/interfaces", methods=["GET"])
def interfaces_report():
    result = InterfacesController.get()

    rendered = render_template("report_base_interfaces.html", interfaces=result)
    return rendered


@reports_router.route("/interfaces/pdf", methods=["GET"])
def interfaces_report_pdf():
    result = InterfacesController.get()

    rendered = render_template("report_base_interfaces.html", interfaces=result)
    pdf = pdfkit.from_string(rendered, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=report.pdf"
    return response
