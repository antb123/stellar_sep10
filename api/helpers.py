from flask_restful import Resource, reqparse
from flask import jsonify, url_for
from werkzeug.exceptions import BadRequest

from datetime import timezone, timedelta
from datetime import datetime as dt
from jwt.exceptions import InvalidTokenError
import settings
import jwt
import time


def validate_jwt(request):
    """
    Validate the JSON web token in a request.
    Return the appropriate error string, or empty string if valid.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('Authorization', required=True, location='headers')
    try:
        request_args = parser.parse_args()
    except BadRequest:
        raise ValueError('No jwt header provided')

    jwt_header = request_args['Authorization']

    if not jwt_header:
        raise ValueError("JWT must be passed as 'Authorization' header")
    if "Bearer" not in jwt_header:
        raise ValueError("'Authorization' header must be formatted as 'Bearer <token>'")

    encoded_jwt = jwt_header.split(" ")[1]
    if not encoded_jwt:
        raise ValueError("'jwt' is required")

    # Validate the JWT contents.
    try:
        jwt_dict = jwt.decode(encoded_jwt, settings.SERVER_JWT_KEY)
    except InvalidTokenError as error:
        raise ValueError("Unable to decode jwt")

    if jwt_dict["iss"] != url_for('sep_auth', _external=True):
        raise ValueError("'jwt' has incorrect 'issuer'")

    if account is not None:
        if jwt_dict["sub"] != account:
            raise ValueError("'jwt' has incorrect 'subject'")

    current_time = time.time()
    if current_time < jwt_dict["iat"] or current_time > jwt_dict["exp"]:
        raise ValueError("'jwt' is no longer valid")

    # TODO: Investigate if we can validate the JTI, a hex-encoded transaction hash.
    return jwt_dict
