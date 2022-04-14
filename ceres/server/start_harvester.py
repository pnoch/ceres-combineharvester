from ceres.util.start_harvester_funcs import get_harvester_connect_peers
from ceres.server.start_harvester_service import run_harvester_service
import os
import pathlib
from typing import Dict

from ceres.consensus.constants import ConsensusConstants
from ceres.consensus.default_constants import DEFAULT_CONSTANTS
from ceres.harvester.harvester import Harvester
from ceres.harvester.harvester_api import HarvesterAPI
from ceres.rpc.harvester_rpc_api import HarvesterRpcApi
from ceres.server.outbound_message import NodeType
# from ceres.server.start_service import run_service
from ceres.types.peer_info import PeerInfo
from ceres.util.config import load_config_cli
# from ceres.util.config import get_all_coin_names, load_config_cli
from ceres.util.default_root import DEFAULT_ROOT_PATH

# See: https://bugs.python.org/issue29288
"".encode("idna")

SERVICE_NAME = "harvester"

# COIN_NAMES = get_all_coin_names()


def service_kwargs_for_harvester(
    root_path: pathlib.Path,
    config: Dict,
    consensus_constants: ConsensusConstants,
) -> Dict:

    connect_peers = get_harvester_connect_peers(root_path)

    overrides = config["network_overrides"]["constants"][config["selected_network"]]
    updated_constants = consensus_constants.replace_str_to_bytes(**overrides)

    harvester = Harvester(root_path, config, updated_constants)
    peer_api = HarvesterAPI(harvester)
    network_id = config["selected_network"]
    kwargs = dict(
        root_path=root_path,
        node=harvester,
        peer_api=peer_api,
        node_type=NodeType.HARVESTER,
        advertised_port=config["port"],
        service_name=SERVICE_NAME,
        server_listen_ports=[config["port"]],
        connect_peers=connect_peers,
        auth_connect_peers=True,
        network_id=network_id,
    )
    if config["start_rpc_server"]:
        kwargs["rpc_info"] = (HarvesterRpcApi, config["rpc_port"])
    return kwargs


def main() -> None:
    config = load_config_cli(DEFAULT_ROOT_PATH, "config.yaml", SERVICE_NAME)
    kwargs = service_kwargs_for_harvester(DEFAULT_ROOT_PATH, config, DEFAULT_CONSTANTS)
    # return run_service(**kwargs)
    return run_harvester_service(**kwargs)


if __name__ == "__main__":
    main()
