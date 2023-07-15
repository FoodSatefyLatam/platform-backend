from flask import Flask, request, jsonify, send_from_directory
from flask_mysqldb import MySQL
from flask_cors import CORS
import os
import json

from urllib.request import urlopen

from authlib.oauth2.rfc7523 import JWTBearerTokenValidator
from authlib.jose.rfc7517.jwk import JsonWebKey
from authlib.integrations.flask_oauth2 import ResourceProtector


class Auth0JWTBearerTokenValidator(JWTBearerTokenValidator):
    def __init__(self, domain, audience):
        issuer = f"https://{domain}/"
        jsonurl = urlopen(f"{issuer}.well-known/jwks.json")
        public_key = JsonWebKey.import_key_set(
            json.loads(jsonurl.read())
        )
        super(Auth0JWTBearerTokenValidator, self).__init__(
            public_key
        )
        self.claims_options = {
            "exp": {"essential": True},
            "aud": {"essential": True, "value": audience},
            "iss": {"essential": True, "value": issuer},
        }

require_auth = ResourceProtector()

validator = Auth0JWTBearerTokenValidator(
    "dev-rqvixarr0an3cp4y.us.auth0.com",
    "OpenCRA-Api"
)

require_auth.register_token_validator(validator)

app = Flask(__name__)
CORS(app)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'grupo1'
app.config['MYSQL_PASSWORD'] = 'gq0xf7vk'
app.config['MYSQL_DB'] = 'grupo1'

mysql = MySQL(app)

import alimentos, calculadora, reporte, contaminantes

if __name__ == "__main__":
    app.run(port = '5001',  host= '0.0.0.0', debug=True, threaded=True)