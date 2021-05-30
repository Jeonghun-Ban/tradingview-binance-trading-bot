import os
from typing import Optional, NamedTuple

from flask import Flask

from binance import Client

from api.utils.config_proxy import load_config
from api.client import MainnetClient, TestnetClient
from api.environment import Environment


class Server(NamedTuple):
    app: Flask
    request: Client


server: Optional[Server] = None


def get_server(env: str = "") -> Server:
    global server
    if server is None:
        app = Flask(__name__)
        app.config.update(load_config(env))
        client = create_client(env=env)

        server = Server(
            app=app,
            request=client,
        )
    return server


def create_client(env: str) -> Client:
    if env == Environment.testing:
        api_key = os.getenv("BINANCE_TESTNET_API_KEY")
        api_secret = os.getenv("BINANCE_TESTNET_SECRET_KEY")
        return TestnetClient(api_key, api_secret)
    else:
        api_key = os.getenv("BINANCE_MAINNET_API_KEY")
        api_secret = os.getenv("BINANCE_MAINNET_SECRET_KEY")
        return MainnetClient(api_key, api_secret)
