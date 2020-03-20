from stellar_sdk.sep.stellar_web_authentication import (
    build_challenge_transaction,
    read_challenge_transaction,
    verify_challenge_transaction_threshold,
    verify_challenge_transaction_signed_by_client_master_key,
)
from stellar_sdk.sep.exceptions import InvalidSep10ChallengeError
from stellar_sdk.exceptions import (
    Ed25519PublicKeyInvalidError,
    NotFoundError,
)
from stellar_sdk.network import Network

from flask_restful import Resource, reqparse
from flask import jsonify, url_for
from werkzeug.exceptions import BadRequest

import jwt
import time
import settings
import binascii
import logging


LOGGER = logging.getLogger('root')


def _get_network_passphrase():
    if settings.STELLAR_NETWORK == 'PUBLIC':
        passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
    else:
        passphrase = Network.TESTNET_NETWORK_PASSPHRASE
    return passphrase


class Sep10Auth(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('account', required=True)
        try:
            request_args = parser.parse_args()
        except BadRequest:
            return jsonify({'error': 'no account provided', 'status': 400})

        account_pubkey = request_args['account']

        try:
            transaction = self._build_challenge(account_pubkey)
        except Ed25519PublicKeyInvalidError as error:
            return jsonify({'error': str(error), 'status': 400})

        LOGGER.info(f"Returning SEP-10 challenge for account {account_pubkey}")
        return jsonify(
            {
                "transaction": transaction,
                "network_passphrase": _get_network_passphrase(),
            }
        )

    @staticmethod
    def _build_challenge(account_pubkey):
        return build_challenge_transaction(
            server_secret=settings.ANCHOR_SIGNING_SECRET,
            client_account_id=account_pubkey,
            anchor_name=settings.ANCHOR_NAME,
            network_passphrase=_get_network_passphrase(),
            timeout=900,
        )

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('transaction', required=True)

        try:
            request_args = parser.parse_args()
        except BadRequest as error:
            return jsonify({'error': 'No request arguments found', 'status': 400})
        else:
            transaction = request_args['transaction']
            if not transaction:
                return jsonify({'error': 'No transaction found', 'status': 400})

        try:
            self._validate_challenge_xdr(transaction)
        except ValueError as error:
            return jsonify({'error': str(error), 'status': 400})
        else:
            return jsonify({'token': self._generate_jwt(transaction)})

    @staticmethod
    def _validate_challenge_xdr(envelope_xdr):
        server_key = settings.ANCHOR_SIGNING_PUBKEY
        network = _get_network_passphrase()

        LOGGER.info("Validating challenge transaction")
        try:
            tx_envelope, account_id = read_challenge_transaction(envelope_xdr, server_key, network)
        except InvalidSep10ChallengeError as error:
            error_msg = f"Error while validating challenge: {str(error)}"
            LOGGER.error(error_msg)
            raise ValueError(error_msg)

        try:
            account = settings.HORIZON_SERVER.load_account(account_id)
        except NotFoundError:
            LOGGER.warning("Account does not exist, using client's master key to verify")
            try:
                verify_challenge_transaction_signed_by_client_master_key(
                    envelope_xdr, server_key, network
                )
            except InvalidSep10ChallengeError as error:
                LOGGER.info(f"Missing or invalid signature(s) for {account_id}: {str(error)})")
                raise ValueError(str(error))
            else:
                LOGGER.info("Challenge verified using client's master key")
                return

        signers = account.load_ed25519_public_key_signers()
        threshold = account.thresholds.med_threshold

        try:
            signers_found = verify_challenge_transaction_threshold(
                envelope_xdr, server_key, network, threshold, signers
            )
        except InvalidSep10ChallengeError as error:
            LOGGER.info(str(error))
            raise ValueError(str(error))

        LOGGER.info(f"Challenge verified using account signers: {signers_found}")

    @staticmethod
    def _generate_jwt(envelope_xdr):
        issued_at = time.time()
        server_key = settings.ANCHOR_SIGNING_PUBKEY
        network = _get_network_passphrase()

        transaction_envelope, source_account = read_challenge_transaction(envelope_xdr, server_key, network)
        LOGGER.info(f"Challenge verified, generating SEP-10 token for account {source_account}")

        hash_hex = binascii.hexlify(transaction_envelope.hash()).decode()
        jwt_dict = {
            "iss": url_for('sep_auth', _external=True),
            "sub": source_account,
            "iat": issued_at,
            "exp": issued_at + 24 * 60 * 60,
            "jti": hash_hex,
        }
        encoded_jwt = jwt.encode(jwt_dict, settings.SERVER_JWT_KEY)
        return encoded_jwt.decode("ascii")

