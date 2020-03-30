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

STELLAR_NETWORK = 'PUBLIC'

HORIZON_URI_DICT = {
    'TESTNET': 'https://horizon-testnet.stellar.org/',
    'PUBLIC': 'https://horizon.stellar.org/',
}
HORIZON_URI = HORIZON_URI_DICT[STELLAR_NETWORK]

ANCHORS = {
    "TEMPO": {
        "WEB_AUTH_ENDPOINT": "https://k.tempo.eu.com/auth",
        "TRANSFER_SERVER": "https://api.tempo.eu.com/t1",
        "DEPOSIT_SERVER": "https://api.tempo.eu.com/v1/deposit",
        "FEDERATION_SERVER": "https://api.tempo.eu.com/v1/federate",
        "SIGNING_KEY": "GCZF7CGJV75G2XNJOONJS5UZMASHPWUVJQMWTVDU5H3BS4OPXLSZ3AUH",
    },
    "COWRIE": {
        "WEB_AUTH_ENDPOINT": "https://api.cowrie.exchange/web_auth",
        "TRANSFER_SERVER": "https://api.cowrie.exchange/transfer",
        "DEPOSIT_SERVER": "",
        "FEDERATION_SERVER": "https://api.cowrie.exchange/federation",
        "SIGNING_KEY": "GBQZOJE2GWJU5VBT6NBLD2F3IOVOYUBDAXYUU32XMHDF4RMDOURWV3GT",
    },
    "APAY": {
        "WEB_AUTH_ENDPOINT": "",
        "TRANSFER_SERVER": "https://api.apay.io/api",
        "DEPOSIT_SERVER": "https://apay.io/api",
        "FEDERATION_SERVER": "https://apay.io/api/federation",
        "SIGNING_KEY": "GD3CS2AR4YZ25LN6NARSSRJMUY7XQBJNGJJTQU2URRDPTPJZBYU2O3DD",
    }
}
