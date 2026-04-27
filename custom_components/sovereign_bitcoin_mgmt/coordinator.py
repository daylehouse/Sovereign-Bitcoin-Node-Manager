from datetime import timedelta
import logging
import aiohttp
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class SovereignBitcoinCoordinator(DataUpdateCoordinator):
    async def _fetch_bitcoind_uptime(self):
        """Fetch uptime from bitcoind via RPC (uptime, returns seconds)."""
        import base64
        import time
        url = f"http://{self.host}:{self.bitcoind_port}/"
        headers = {}
        if self.bitcoind_rpc_user and self.bitcoind_rpc_password:
            userpass = f"{self.bitcoind_rpc_user}:{self.bitcoind_rpc_password}"
            headers["Authorization"] = "Basic " + base64.b64encode(userpass.encode()).decode()
        payload = {"jsonrpc": "1.0", "id": "hass", "method": "uptime", "params": []}
        try:
            async with self.session.post(url, json=payload, headers=headers, timeout=10) as resp:
                if resp.status == 200:
                    rpc_result = await resp.json()
                    seconds = rpc_result.get("result")
                    if isinstance(seconds, int):
                        # Return boot time as UTC timestamp
                        return int(time.time()) - seconds
                else:
                    _LOGGER.error(f"Bitcoind uptime error: {resp.status}")
        except Exception as e:
            _LOGGER.error(f"Error fetching bitcoind uptime: {e}")
        return None

    async def _fetch_bitcoind_sync_state(self):
        """Fetch the blockchain sync state from bitcoind via RPC."""
        import base64
        url = f"http://{self.host}:{self.bitcoind_port}/"
        headers = {}
        if self.bitcoind_rpc_user and self.bitcoind_rpc_password:
            userpass = f"{self.bitcoind_rpc_user}:{self.bitcoind_rpc_password}"
            headers["Authorization"] = "Basic " + base64.b64encode(userpass.encode()).decode()
        payload = {"jsonrpc": "1.0", "id": "hass", "method": "getblockchaininfo", "params": []}
        try:
            async with self.session.post(url, json=payload, headers=headers, timeout=10) as resp:
                if resp.status == 200:
                    rpc_result = await resp.json()
                    return rpc_result.get("result", {})
                else:
                    _LOGGER.error(f"Bitcoind RPC error: {resp.status}")
        except Exception as e:
            _LOGGER.error(f"Error fetching bitcoind sync state: {e}")
        return None

    async def _fetch_bitcoind_network_info(self):
        """Fetch network info from bitcoind via RPC (getnetworkinfo)."""
        import base64
        url = f"http://{self.host}:{self.bitcoind_port}/"
        headers = {}
        if self.bitcoind_rpc_user and self.bitcoind_rpc_password:
            userpass = f"{self.bitcoind_rpc_user}:{self.bitcoind_rpc_password}"
            headers["Authorization"] = "Basic " + base64.b64encode(userpass.encode()).decode()
        payload = {"jsonrpc": "1.0", "id": "hass", "method": "getnetworkinfo", "params": []}
        try:
            async with self.session.post(url, json=payload, headers=headers, timeout=10) as resp:
                if resp.status == 200:
                    rpc_result = await resp.json()
                    return rpc_result.get("result", {})
                else:
                    _LOGGER.error(f"Bitcoind getnetworkinfo error: {resp.status}")
        except Exception as e:
            _LOGGER.error(f"Error fetching bitcoind network info: {e}")
        return None

    async def _fetch_bitcoind_peer_info(self):
        """Fetch peer info from bitcoind via RPC (getpeerinfo)."""
        import base64
        url = f"http://{self.host}:{self.bitcoind_port}/"
        headers = {}
        if self.bitcoind_rpc_user and self.bitcoind_rpc_password:
            userpass = f"{self.bitcoind_rpc_user}:{self.bitcoind_rpc_password}"
            headers["Authorization"] = "Basic " + base64.b64encode(userpass.encode()).decode()
        payload = {"jsonrpc": "1.0", "id": "hass", "method": "getpeerinfo", "params": []}
        try:
            async with self.session.post(url, json=payload, headers=headers, timeout=10) as resp:
                if resp.status == 200:
                    rpc_result = await resp.json()
                    return rpc_result.get("result", [])
                else:
                    _LOGGER.error(f"Bitcoind getpeerinfo error: {resp.status}")
        except Exception as e:
            _LOGGER.error(f"Error fetching bitcoind peer info: {e}")
        return []

    def __init__(self, hass: HomeAssistant, host: str, btc_addresses: str = None, public_pool_port: int = 3334, bitcoind_port: int = 8332, bitcoind_rpc_user: str = None, bitcoind_rpc_password: str = None):
        super().__init__(
            hass,
            _LOGGER,
            name="Sovereign Bitcoin Node Data",
            update_interval=timedelta(seconds=30),
        )
        self.host = host
        self.btc_addresses = btc_addresses
        self.public_pool_port = public_pool_port
        self.session = aiohttp.ClientSession()
        self.bitcoind_port = bitcoind_port
        self.bitcoind_rpc_user = bitcoind_rpc_user
        self.bitcoind_rpc_password = bitcoind_rpc_password

    async def _async_update_data(self):
        data = {}
        explorer_port = getattr(self, "bitcoin_explorer_port", 3020)
        host = self.host
        # Next Halving
        try:
            url = f"http://{host}:{explorer_port}/api/blockchain/next-halving"
            async with self.session.get(url, timeout=10) as resp:
                if resp.status == 200:
                    data["next_halving"] = await resp.json()
                else:
                    data["next_halving"] = None
        except Exception as e:
            _LOGGER.error("Error fetching next halving: %s", e)
            data["next_halving"] = None

        # Block Tip
        try:
            url = f"http://{host}:{explorer_port}/api/blocks/tip"
            async with self.session.get(url, timeout=10) as resp:
                if resp.status == 200:
                    data["block_tip"] = await resp.json()
                else:
                    data["block_tip"] = None
        except Exception as e:
            _LOGGER.error("Error fetching block tip: %s", e)
            data["block_tip"] = None

        # Current Block Header (needs block tip height)
        block_tip_height = data.get("block_tip", {}).get("height")
        if block_tip_height is not None:
            try:
                url = f"http://{host}:{explorer_port}/api/block/header/{block_tip_height}"
                async with self.session.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        data["current_block_header"] = await resp.json()
                    else:
                        data["current_block_header"] = None
            except Exception as e:
                _LOGGER.error("Error fetching current block header: %s", e)
                data["current_block_header"] = None
        else:
            data["current_block_header"] = None

        # Bitcoin Explorer getblockchaininfo
        try:
            url = f"http://{host}:{explorer_port}/api/getblockchaininfo"
            async with self.session.get(url, timeout=10) as resp:
                if resp.status == 200:
                    data["blockchaininfo"] = await resp.json()
                else:
                    data["blockchaininfo"] = None
        except Exception as e:
            _LOGGER.error("Error fetching getblockchaininfo: %s", e)
            data["blockchaininfo"] = None

        # Public Pool stats (if BTC address provided)
        miner = self.btc_addresses
        if miner:
            try:
                url = f"http://{host}:{self.public_pool_port}/api/pool?miner={miner}"
                headers = {"User-Agent": "Home Assistant", "Accept": "application/json"}
                async with self.session.get(url, headers=headers, timeout=10) as resp:
                    if resp.status == 200:
                        data["public_pool"] = await resp.json()
                    else:
                        data["public_pool"] = None
            except Exception as e:
                _LOGGER.error("Error fetching public pool stats: %s", e)
                data["public_pool"] = None
        else:
            data["public_pool"] = None

        # Mempool REST API
        try:
            mempool_url = f"http://{host}:4080/api/v1/fees/recommended"
            async with self.session.get(mempool_url, timeout=10) as resp:
                if resp.status == 200:
                    data["mempool_fees"] = await resp.json()
                else:
                    data["mempool_fees"] = None
        except Exception as e:
            _LOGGER.error("Error fetching mempool fees: %s", e)
            data["mempool_fees"] = None

        try:
            mempool_url = f"http://{host}:4080/api/v1/blocks"
            async with self.session.get(mempool_url, timeout=10) as resp:
                if resp.status == 200:
                    data["mempool_blocks"] = await resp.json()
                else:
                    data["mempool_blocks"] = None
        except Exception as e:
            _LOGGER.error("Error fetching mempool blocks: %s", e)
            data["mempool_blocks"] = None

        # Mempool prices
        try:
            mempool_url = f"http://{host}:4080/api/v1/prices"
            async with self.session.get(mempool_url, timeout=10) as resp:
                if resp.status == 200:
                    data["mempool_prices"] = await resp.json()
                else:
                    data["mempool_prices"] = None
        except Exception as e:
            _LOGGER.error("Error fetching mempool prices: %s", e)
            data["mempool_prices"] = None

        # Bitcoind sync state
        data["bitcoind_sync_state"] = await self._fetch_bitcoind_sync_state()

        # Bitcoind network info (version, peer counts)
        network_info = await self._fetch_bitcoind_network_info()
        data["bitcoind_network_info"] = network_info

        # Bitcoind peer info (for incoming/outgoing peer counts)
        peer_info = await self._fetch_bitcoind_peer_info()
        data["bitcoind_peer_info"] = peer_info

        # Aggregate peer counts
        incoming = 0
        outgoing = 0
        for peer in peer_info:
            if peer.get("inbound"):
                incoming += 1
            else:
                outgoing += 1
        data["bitcoind_peers_incoming"] = incoming
        data["bitcoind_peers_outgoing"] = outgoing

        # Sync progress and blocks (from sync state)
        sync_state = data["bitcoind_sync_state"] or {}
        data["bitcoind_sync_progress"] = sync_state.get("verificationprogress")
        data["bitcoind_blocks"] = sync_state.get("blocks")
        data["bitcoind_headers"] = sync_state.get("headers")

        # Bitcoind version
        if network_info:
            data["bitcoind_version"] = network_info.get("subversion")
        else:
            data["bitcoind_version"] = None

        # Bitcoind uptime (boot time as timestamp)
        data["bitcoind_uptime"] = await self._fetch_bitcoind_uptime()
        return data
