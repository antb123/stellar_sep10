from stellar_sdk.server import Server
from stellar_sdk.keypair import Keypair
from logging.config import dictConfig
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'tsmthandler': {
            'level':'INFO',
            'formatter': 'default',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'TSMT.log'),
            'maxBytes': 1024*1024*15, # 15MB
            'backupCount': 10,
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['tsmthandler']
    }
})



SEP10AUTH = True

STELLAR_NETWORK = 'TESTNET'

HORIZON_URI_DICT = {
    'TESTNET': 'https://horizon-testnet.stellar.org/',
    'PUBLIC': 'https://horizon.stellar.org/',
}
HORIZON_URI = HORIZON_URI_DICT[STELLAR_NETWORK]
HORIZON_SERVER = Server(horizon_url=HORIZON_URI)

# kp = Keypair.random()
# ANCHOR_SIGNING_SECRET = kp.secret
# ANCHOR_SIGNING_PUBKEY = Keypair.from_secret(ANCHOR_SIGNING_SECRET).public_key

ANCHOR_DISTRIBUTION_ACCOUNTS = {
    "PURPLE": {
        "pubkey": "GBT4VVTDPCNA45MNWX5G6LUTLIEENSTUHDVXO2AQHAZ24KUZUPLPGJZH", # distribution account pubkey
        "secret": "SAIZO63I4X2MWWSGUWBDHWDYCLYCIXGMM2CN4GO2IIHWYSLQBKISFKBQ", # distribution account secret
        "asset_code": "PURPLE", # asset holded by this account
        "issuer": "GBT4VVTDPCNA45MNWX5G6LUTLIEENSTUHDVXO2AQHAZ24KUZUPLPGJZH", # asset issuer
        "stellar_toml": None, # a stellar.toml for reference
    }
}

ANCHOR_NAME = 'TEMPO FRANCE'
ANCHOR_SIGNING_PUBKEY = "GCXDABO7BOKAFDV3KI6U6WO6ZZVEREBNFRF4KIFHSWLEKZ424OG32UDV"
ANCHOR_SIGNING_SECRET = "SCY7NNDNR4477JWI5YGXABT6N4MC3I2WUH66SGEWKU6SEYNBXP5EPVH3"

ANCHOR_ISSUING_PUBKEY = "GBT4VVTDPCNA45MNWX5G6LUTLIEENSTUHDVXO2AQHAZ24KUZUPLPGJZH"

ANCHOR_ASSETS = {
    "PURPLE": {
        "deposit_enabled": True,
        "deposit_fee_fixed": 1.0,
        "deposit_fee_percent": 0.01,
        "deposit_min_amount": 10.0,
        "deposit_max_amount": 10000.0,
        "withdrawal_enabled": True,
        "withdrawal_fee_fixed": 1.0,
        "withdrawal_fee_percent": 0.01,
        "withdrawal_min_amount": 10.0,
        "withdrawal_max_amount": 10000.0,
        "transaction_enabled": True,
        "transactions_enabled": True,
    },
    "EURT": {
        "deposit_enabled": False,
        "deposit_fee_fixed": 1.0,
        "deposit_fee_percent": 0.01,
        "deposit_min_amount": 10.0,
        "deposit_max_amount": 10000.0,
        "withdrawal_enabled": True,
        "withdrawal_fee_fixed": 1.0,
        "withdrawal_fee_percent": 0.01,
        "withdrawal_min_amount": 10.0,
        "withdrawal_max_amount": 10000.0,
        "transaction_enabled": True,
        "transactions_enabled": True,
    }
}

SERVER_JWT_KEY = 'secret'

SERVER_JWT_PUBKEY = """
-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA0yX6N1ifVuKta4Zc9VG8
UB5VsuwC23fUbfGoNivlQr21Qul073v5aF8zdHeVfNk9M++Q1of0WkqS/qH9DkFB
aD2/C8J+L4L9If8vQyl7u/TEJVWrBS0G4WZcVbPWHfJ4fqa0TaOwMiR4dlaGkjUI
qnnPJEjpI7EkfkXo3ggWe4Oo6436VFusuW389ZKOmBTR8dAYtCU1ArAa5r7cEbw6
OG1PLt4sOWGmiBwZXoxGlK4y9LkVPqAdOmRwBbgD0CkhZSq6v3cP6dRP6WSKgCRE
H15uIIwKeMowpnLwZMA+isGJPK4yjKriO3oS4VgYaqukHqg/O5RpbtVJgRotstGE
xFFEtrBNWjDAIaRk5xBXQdNq2ktMH52UmZ93X92uEDAZgCKa9aQbuj4NQxsWiEGQ
BZLRnV0uKD2R6U0JVLQvc3UbDYwRts5T22cqnPtSpbV808c6D4YJxaGXZ5kweY2q
mPGER57ixx8BBRLkh+hVGVeiz/2EPaiB2SbXLTkZ+jWwfyIsHT3BWarl/fiJrcwn
e+nwosTY8LSmqOeVvtAFPO5hya2KwGO4Vpgesc5tCAF3OlXekkmr0UfOrhdVEPjy
H7I66kofGeztByGVKg6TXbn5DshKcJbmhN4tuhmr2nGkwUYY7c9fXU7yhaS7+lyZ
pXOrHT0isq3sRFFMcjquhSsCAwEAAQ==
-----END PUBLIC KEY-----
"""
SERVER_JWT_SECRET = """
-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----
"""