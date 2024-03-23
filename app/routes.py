from flask import Blueprint, request, jsonify
from .cyanite.views import handle_webhook, upload_file

main = Blueprint('main', __name__)


@main.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    handle_webhook(data)
    return jsonify(success=True), 200


@main.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    response = upload_file(file)
    return jsonify(response), 200
