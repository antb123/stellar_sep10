from flask_restful import reqparse
from flask import jsonify, url_for
from werkzeug.exceptions import BadRequest

from datetime import timezone, timedelta
from datetime import datetime as dt
from jwt.exceptions import InvalidTokenError
import settings
import jwt
import time


def check_auth(func):
    try:
        account = validate_jwt_request()
    except ValueError as error:
        return jsonify({'error': str(error), 'status': 403})

    return func(account)


def validate_sep10_token(view):
    def wrapper(*args, **kwargs):
        return check_auth(view)

    return wrapper


def validate_jwt_request():
    """
    Validate the JSON web token in a request.
    Return the appropriate error string, or empty string if valid.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('Authorization', required=True, location='headers')
    try:
        request_args = parser.parse_args()
    except BadRequest:
        raise ValueError('No Authorization header provided')

    bad_format_error = ValueError(
        "'Authorization' header must be formatted as 'Bearer <token>'"
    )

    jwt_header = request_args['Authorization']

    if not jwt_header:
        raise bad_format_error
    if "Bearer" not in jwt_header:
        raise bad_format_error

    try:
        encoded_jwt = jwt_header.split(" ")[1]
    except IndexError:
        raise bad_format_error

    if not encoded_jwt:
        raise ValueError("'jwt' is required")

    # Validate the JWT contents.
    try:
        jwt_dict = jwt.decode(encoded_jwt, settings.SERVER_JWT_KEY)
    except InvalidTokenError as error:
        raise ValueError("Unable to decode jwt")

    if jwt_dict["iss"] != url_for('sep_auth', _external=True):
        raise ValueError("'jwt' has incorrect 'issuer'")

    # if account is not None:
    #     if jwt_dict["sub"] != account:
    #         raise ValueError("'jwt' has incorrect 'subject'")

    current_time = time.time()
    if current_time < jwt_dict["iat"] or current_time > jwt_dict["exp"]:
        raise ValueError("'jwt' is no longer valid")

    # TODO: Investigate if we can validate the JTI, a hex-encoded transaction hash.
    try:
        return jwt_dict["sub"]
    except KeyError:
        raise ValueError("Decoded JWT missing 'sub' field")
