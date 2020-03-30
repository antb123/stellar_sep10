from flask import Blueprint, jsonify, Response
from werkzeug.exceptions import BadRequest
from flask_restful import reqparse
import requests
import settings
import logging


info_mod = Blueprint('info_mod', __name__)
LOGGER = logging.getLogger('root')


@info_mod.route('/api/info')
def get_anchor_info():
    parser = reqparse.RequestParser()
    parser.add_argument('anchor', required=True)
    try:
        request_args = parser.parse_args()
    except BadRequest:
        err_msg = 'Not enough arguments provided'
        LOGGER.error(err_msg)
        return jsonify({'error': err_msg, 'status': 400})

    anchor_name = request_args['anchor']
    anchor_name = settings.ANCHORS[anchor_name]

    try:
        response = requests.get(anchor_name['TRANSFER_SERVER'] + '/info')
    except requests.exceptions.RequestException as error:
        LOGGER.error(error)
        return jsonify({'status': 400, 'error': str(error)})

    return response.json()