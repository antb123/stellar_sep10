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
from stellar_sdk.keypair import Keypair

from flask_restful import Resource, Api, reqparse
from flask import Flask, request, jsonify

import os
import jwt
import json
import time
import settings
import binascii
from urllib.parse import parse_qsl


app = Flask(__name__)
api = Api(app)


class Sep10Auth(Resource):
    def get(self):
        # pubkey = 'GAP5LETOV6YIE62YяAM56STDANPRDO7ZFDBGSNHJQIYGGKSMOZAHOOS2S'

        pubkey = settings.SIGNING_KEY
        secret = settings.SIGNING_SEED

        network = settings.STELLAR_NETWORK_PASSPHRASE
        timeout = 900
        anchor = 'tempo.eu.com'

        try:
            transaction = self._build_challenge(secret, pubkey, anchor, network, timeout)
        except Exception as error:
            return jsonify({'error': str(error), 'status': 400})

        return jsonify(
            {
                "transaction": transaction,
                "network_passphrase": settings.STELLAR_NETWORK_PASSPHRASE,
            }
        )

    @staticmethod
    def _build_challenge(server_secret, client_account_id, anchor_name, network_passphrase, timeout):
        return build_challenge_transaction(
            server_secret,
            client_account_id,
            anchor_name,
            network_passphrase,
            timeout,
        )

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('transaction', required=True)
        parser.add_argument('Content-Type', required=True, location='headers')
        request_args = parser.parse_args()

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
        server_key = settings.SIGNING_KEY
        network = settings.STELLAR_NETWORK_PASSPHRASE

        try:
            tx_envelope, account_id = read_challenge_transaction(envelope_xdr, server_key, network)
        except InvalidSep10ChallengeError as error:
            error_msg = f"Error while validating challenge: {str(error)}"
            raise ValueError(error_msg)

        try:
            account = settings.HORIZON_SERVER.load_account(account_id)
        except NotFoundError:
            print("Account does not exist, using client's master key to verify")
            try:
                verify_challenge_transaction_signed_by_client_master_key(
                    envelope_xdr, server_key, network
                )
            except InvalidSep10ChallengeError as error:
                raise ValueError(str(error))
            else:
                return "Challenge verified using client's master key"

        signers = account.load_ed25519_public_key_signers()
        threshold = account.thresholds.med_threshold

        try:
            signers_found = verify_challenge_transaction_threshold(
                envelope_xdr, server_key, network, threshold, signers
            )
        except InvalidSep10ChallengeError as error:
            raise ValueError(str(error))

        print(f"Challenge verified using account signers: {signers_found}")

    @staticmethod
    def _generate_jwt(envelope_xdr):
        issued_at = time.time()
        transaction_envelope, source_account = read_challenge_transaction(
            envelope_xdr, settings.SIGNING_KEY, settings.STELLAR_NETWORK_PASSPHRASE
        )
        print(f"Challenge verified, generating SEP-10 token for account {source_account}")

        hash_hex = binascii.hexlify(transaction_envelope.hash()).decode()
        jwt_dict = {
            "iss": os.path.join(settings.HOST_URL, "auth"),
            "sub": source_account,
            "iat": issued_at,
            "exp": issued_at + 24 * 60 * 60,
            "jti": hash_hex,
        }
        encoded_jwt = jwt.encode(jwt_dict, settings.SERVER_JWT_KEY, algorithm="HS256")
        return encoded_jwt.decode("ascii")


api.add_resource(Sep10Auth, '/api/sep_auth')


if __name__ == '__main__':
    app.run(debug=True)