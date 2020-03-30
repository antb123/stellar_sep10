from flask import Blueprint, jsonify
from flask_restful import reqparse
from werkzeug.exceptions import BadRequest

import requests
import settings
import logging


withdraw_mod = Blueprint('withdraw_mod', __name__)
LOGGER = logging.getLogger('root')


@withdraw_mod.route('/api/withdraw')
def deposit():
    parser = reqparse.RequestParser()
    parser.add_argument('asset_code', required=True)
    parser.add_argument('anchor', required=True)
    parser.add_argument('email', required=True)
    parser.add_argument('Authorization', required=True, location='headers')

    try:
        request_args = parser.parse_args()
    except BadRequest:
        err_msg = 'Not enough arguments provided'
        LOGGER.error(err_msg)
        return jsonify({'error': err_msg, 'status': 400})

    asset_code = request_args['asset_code']
    anchor_name = request_args['anchor']
    account_email = request_args['email']
    token = request_args['Authorization']

    try:
        anchor_name = settings.ANCHORS[anchor_name]
    except KeyError:
        err_msg = "No such anchor"
        LOGGER.error(err_msg)
        return jsonify({"error": err_msg, "status": 404})


    url = anchor_name['TRANSFER_SERVER'] + '/withdraw'
    params = {
        'asset_code': asset_code,
        'email_address': account_email,
    }
    headers = {
        'Authorization': token,
    }

    try:
        response = requests.get(url, params=params, headers=headers)
    except requests.exceptions.RequestException as error:
        LOGGER.error(error)
        return jsonify({'status': 400, 'error': str(error)})
    
    withdraw_info = response.json()
    return jsonify({'response': withdraw_info, 'status': response.status_code})