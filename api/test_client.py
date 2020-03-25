import json
import sys
import requests
from getpass import getpass
from stellar_base.keypair import Keypair
from stellar_base.stellarxdr import Xdr
from stellar_base.transaction_envelope import TransactionEnvelope

if len(sys.argv) < 3:
    print(f'usage: {sys.argv[0]} server_url public_key')
    print(f'example: {sys.argv[0]} server_url public_key')
    sys.exit(1)

server_url = sys.argv[1]
public_key = sys.argv[2]

secret_key = getpass("Secret key (won't be displayed): ")

response = requests.get(f"{server_url}/auth?account={public_key}")
content = json.loads(response.content)
envelope_xdr = content["transaction"]
envelope_object = TransactionEnvelope.from_xdr(envelope_xdr)
client_signing_key = Keypair.from_seed(secret_key)
envelope_object.sign(client_signing_key)
client_signed_envelope_xdr = envelope_object.xdr().decode("ascii")
response = requests.post(f"{server_url}/auth", json={"transaction": client_signed_envelope_xdr})
content = json.loads(response.content)

print(content["token"])
