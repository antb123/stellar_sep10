from stellar_sdk.server import Server
from stellar_sdk.keypair import Keypair


STELLAR_ANCHORS = {
    'naobtc.com': {
        'assets': {
            'BTC': 'GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH',
        },
    },
    'tempo.eu.com': {
        'assets': {
            'EURT': 'GAP5LETOV6YIE62YAM56STDANPRDO7ZFDBGSNHJQIYGGKSMOZAHOOS2S',
            'LKR': 'GAP5LETOV6YIE62YAM56STDANPRDO7ZFDBGSNHJQIYGGKSMOZAHOOS2S',
            'XOF': 'GAP5LETOV6YIE62YAM56STDANPRDO7ZFDBGSNHJQIYGGKSMOZAHOOS2S',
            'XAF': 'GAP5LETOV6YIE62YAM56STDANPRDO7ZFDBGSNHJQIYGGKSMOZAHOOS2S',
        },
        'signing_pubkey': 'GCZF7CGJV75G2XNJOONJS5UZMASHPWUVJQMWTVDU5H3BS4OPXLSZ3AUH',
    }
}


# STELLAR_NETWORK = 'TESTNET'
STELLAR_NETWORK_PASSPHRASE = "Public Global Stellar Network ; September 2015"

# HORIZON_URI_DICT = {
#     'TESTNET': 'https://horizon-testnet.stellar.org/',
#     'PUBLIC': 'https://horizon.stellar.org/',
# }
HORIZON_URI = 'https://horizon-testnet.stellar.org/'
HORIZON_SERVER = Server(horizon_url=HORIZON_URI)

kp = Keypair.random()
SIGNING_SEED = kp.secret
SIGNING_KEY = Keypair.from_secret(SIGNING_SEED).public_key

SERVER_JWT_KEY = 'secret'
HOST_URL = 'http://testtsmt.tempo.eu.com'