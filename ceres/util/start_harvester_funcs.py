from ceres.server.server import ssl_context_for_client
from ceres.server.ssl_context import private_ssl_ca_paths, private_ssl_paths
from ceres.util.default_root import get_coin_root_path
from ceres.util.ceres_config import get_coin_config, get_mining_coin_names
from ceres.server.server import ssl_context_for_client

def ssl_context_for_coin(coin: str):

    coin_root_path = get_coin_root_path(coin)
    coin_config = get_coin_config(coin, "harvester")

    _private_cert_path, _private_key_path = private_ssl_paths(coin_root_path, coin_config)
    ca_private_crt_path, ca_private_key_path = private_ssl_ca_paths(coin_root_path, coin_config)

    ssl_context = ssl_context_for_client(
        ca_private_crt_path, ca_private_key_path, _private_cert_path, _private_key_path
    )

    return ssl_context