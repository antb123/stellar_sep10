from stellar_sdk.sep.stellar_web_authentication import read_challenge_transaction
from stellar_sdk.exceptions import Ed25519SecretSeedInvalidError
from stellar_sdk.sep.exceptions import InvalidSep10ChallengeError
from stellar_sdk.network import Network
from stellar_sdk import Keypair

from flask import Blueprint, jsonify
from flask_restful import reqparse
from werkzeug.exceptions import BadRequest

import requests
import settings
import logging
import json


sep10_mod = Blueprint('sep10_mod', __name__)
LOGGER = logging.getLogger('root')


class BadAccountId(Exception):
    pass


def _get_network_passphrase():
    if settings.STELLAR_NETWORK == 'PUBLIC':
        passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
    else:
        passphrase = Network.TESTNET_NETWORK_PASSPHRASE
    return passphrase


@sep10_mod.route('/api/auth')
def get_transaction():
    parser = reqparse.RequestParser()
    parser.add_argument('account', required=True)
    parser.add_argument('secret', required=True)
    parser.add_argument('anchor', required=True)

    try:
        request_args = parser.parse_args()
    except BadRequest:
        err_msg = 'Not enough arguments provided'
        LOGGER.error(err_msg)
        return jsonify({'error': err_msg, 'status': 400})

    account_pubkey = request_args['account']
    account_secret = request_args['secret']
    anchor_name = request_args['anchor']

    try:
        anchor_name = settings.ANCHORS[anchor_name]
    except KeyError:
        err_msg = "No such anchor"
        LOGGER.error(err_msg)
        return jsonify({"error": err_msg, "status": 404})

    url = anchor_name['WEB_AUTH_ENDPOINT']
    params = {'account': account_pubkey}

    try:
        transaction_xdr = _get_transaction(url, params)
        transaction_envelope = _check_server_transaction(transaction_xdr, anchor_name)
        signed_transaction= _sign_transaction(transaction_envelope, account_secret)
        token = _get_token(signed_transaction, anchor_name)
    except ValueError as error:
        LOGGER.error(error)
        return jsonify({'error': str(error), 'status': 400})
    else:
        return token


def _get_transaction(url, params):
    LOGGER.info("Getting challenge transaction")
    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise BadAccountId("Bad Account Id")
    except (requests.exceptions.RequestException, BadAccountId) as error:
        raise ValueError(error)

    transaction_xdr = (response.json())['transaction']
    return transaction_xdr


def _check_server_transaction(transaction_xdr, anchor_name):
    LOGGER.info("Validating challenge transaction")
    try:
        transaction_envelope, account_id = read_challenge_transaction(
            transaction_xdr, 
            anchor_name['SIGNING_KEY'], 
            _get_network_passphrase(),
        )
    except InvalidSep10ChallengeError as error:
        raise ValueError(error)

    return transaction_envelope


def _sign_transaction(transaction_envelope, account_secret):
    LOGGER.info("Signing transaction")
    source_kp = Keypair.from_secret(account_secret)

    try:
        transaction_envelope.sign(source_kp)
    except Ed25519SecretSeedInvalidError as error:
        raise ValueError(error)

    signed_transaction = transaction_envelope.to_xdr()
    return signed_transaction


def _get_token(signed_transaction, anchor_name):
    LOGGER.info("Getting token")
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"transaction": signed_transaction})
    url = anchor_name['WEB_AUTH_ENDPOINT']

    try:
        response = requests.post(url, data=data, headers=headers)
    except requests.exceptions.RequestException as error:
        raise ValueError(error)

    return response.json()
