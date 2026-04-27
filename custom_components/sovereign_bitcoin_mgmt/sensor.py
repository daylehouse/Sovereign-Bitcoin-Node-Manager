
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
import datetime
import logging
_LOGGER = logging.getLogger(__name__)

# Mempool price sensors
MEMPOOL_PRICE_STATS = [
    ("USD", "mdi:currency-usd"),
    ("EUR", "mdi:currency-eur"),
    ("GBP", "mdi:currency-gbp"),
    ("CAD", "mdi:currency-cad"),
    ("CHF", "mdi:currency-chf"),
    ("AUD", "mdi:currency-aud"),
    ("JPY", "mdi:currency-jpy"),
]

class MempoolPriceSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, stat_key, icon):
        super().__init__(coordinator)
        self._stat_key = stat_key
        # Map ISO code to correct MDI icon
        currency_icons = {
            "USD": "mdi:currency-usd",
            "EUR": "mdi:currency-eur",
            "GBP": "mdi:currency-gbp",
            "CAD": "mdi:currency-usd",  # Use USD icon for CAD
            "CHF": "mdi:currency-fra",  # Use Franc icon for CHF
            "AUD": "mdi:currency-usd",  # Use USD icon for AUD
            "JPY": "mdi:currency-jpy",
        }
        self._attr_icon = currency_icons.get(stat_key, "mdi:cash")
        self._attr_name = f"Mempool Rate {stat_key}"
        self._attr_unique_id = f"mempool_price_{stat_key}"
        self._attr_device_class = "monetary"
        self._attr_unit_of_measurement = stat_key
        self._attr_currency = stat_key

    @property
    def native_value(self):
        data = self.coordinator.data.get("mempool_prices")
        if data and self._stat_key in data:
            return data[self._stat_key]
        return None

    @property
    def available(self):
        data = self.coordinator.data.get("mempool_prices")
        return data is not None and self._stat_key in data

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "mempool")},
            "name": "Mempool",
            "manufacturer": "Sovereign Bitcoin Node",
            "model": "Mempool REST API",
        }

# Mempool REST API sensors
MEMPOOL_STATS = [
    ("fastestFee", "mdi:rocket"),
    ("halfHourFee", "mdi:clock-fast"),
    ("hourFee", "mdi:clock-outline"),
]

class MempoolFeeSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, stat_key, icon):
        super().__init__(coordinator)
        self._stat_key = stat_key
        self._attr_icon = icon
        self._attr_name = f"Mempool {stat_key.replace('_', ' ').title()}"
        self._attr_unique_id = f"mempool_{stat_key}"

    @property
    def native_value(self):
        data = self.coordinator.data.get("mempool_fees")
        if data and self._stat_key in data:
            return data[self._stat_key]
        return None

    @property
    def available(self):
        data = self.coordinator.data.get("mempool_fees")
        return data is not None and self._stat_key in data

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "mempool")},
            "name": "Mempool",
            "manufacturer": "Sovereign Bitcoin Node",
            "model": "Mempool REST API",
        }
from .const import DOMAIN
import datetime
import logging
_LOGGER = logging.getLogger(__name__)

# Bitcoin Explorer getindexinfo fields
BITCOIN_EXPLORER_INDEX_STATS = [
    # All BTC Explorer index sensors removed
]

class BitcoinExplorerIndexStatSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, stat_key, icon):
        super().__init__(coordinator)
        self._stat_key = stat_key
        self._attr_icon = icon
        self._attr_name = f"Bitcoin Explorer {stat_key.replace('_', ' ').title()}"
        self._attr_unique_id = f"btc_explorer_{stat_key}"

    @property
    def native_value(self):
        data = self.coordinator.data.get("indexinfo")
        if data is not None and "txindex" in data:
            if self._stat_key == "txindex_synced":
                return bool(data["txindex"].get("synced"))
            if self._stat_key == "txindex_best_block_height":
                try:
                    return int(data["txindex"].get("best_block_height"))
                except Exception:
                    return data["txindex"].get("best_block_height")
        return None

    @property
    def available(self):
        data = self.coordinator.data.get("indexinfo")
        return data is not None and "txindex" in data

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "bitcoin_explorer")},
            "name": "Bitcoin Explorer",
            "manufacturer": "Sovereign Bitcoin Node",
            "model": "Bitcoin Explorer API",
        }


from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
import datetime

# Dynamically create a sensor for each mining pool stat (matching actual API keys)
MINING_POOL_STATS = [
    ("totalHashRate", "mdi:pickaxe"),
    ("blockHeight", "mdi:cube-outline"),
    ("totalMiners", "mdi:account-group"),
    ("blocksFound", "mdi:cube-scan"),
    ("fee", "mdi:cash"),
]


import logging
_LOGGER = logging.getLogger(__name__)


class SoloPoolStatSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, stat_key, icon):
        super().__init__(coordinator)
        self._stat_key = stat_key
        self._attr_icon = icon
        self._attr_name = f"Solo Pool {stat_key.replace('_', ' ').title()}"
        self._attr_unique_id = f"btc_solo_pool_{stat_key}"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "solo_pool")},
            "name": "Solo Pool",
            "manufacturer": "Sovereign Bitcoin Node",
            "model": "Solo Pool API",
        }

    @property
    def native_value(self):
        data = self.coordinator.data.get("public_pool")
        if data is not None:
            _LOGGER.debug(f"MiningPoolStatSensor: public_pool payload: {data}")
            if self._stat_key in data:
                value = data[self._stat_key]
                # If value is a list, return its length
                if isinstance(value, list):
                    return len(value)
                # Format specific stats
                if self._stat_key == "totalMiners":
                    try:
                        return int(value)
                    except Exception:
                        return value
                if self._stat_key == "blockHeight":
                    try:
                        return int(value)
                    except Exception:
                        return value
                if self._stat_key == "totalHashRate":
                    try:
                        # Convert from H/s to TH/s
                        return round(float(value) / 1e12, 2)
                    except Exception:
                        return value
                # Try to cast to float or int if possible
                try:
                    if isinstance(value, str) and value.isdigit():
                        return int(value)
                    return float(value)
                except Exception:
                    return value
        _LOGGER.debug(f"MiningPoolStatSensor: No data for {self._stat_key}")
        return None

    @property
    def available(self):
        data = self.coordinator.data.get("public_pool")
        return data is not None and self._stat_key in data

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

# File must be named sensor.py for Home Assistant to load the sensor platform correctly.


# Bitcoin Explorer stats (getblockchaininfo fields)
BITCOIN_EXPLORER_STATS = [
    # All BTC Explorer sensors removed
]

class BitcoinExplorerStatSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, stat_key, icon):
        super().__init__(coordinator)
        self._stat_key = stat_key
        self._attr_icon = icon
        self._attr_name = f"Bitcoin Explorer {stat_key.replace('_', ' ').title()}"
        self._attr_unique_id = f"btc_explorer_{stat_key}"

    @property
    def native_value(self):
        data = self.coordinator.data.get("blockchaininfo")
        if data is not None and self._stat_key in data:
            value = data[self._stat_key]
            # Format specific stats
            if self._stat_key in ("blocks", "headers", "size_on_disk"):
                try:
                    return int(value)
                except Exception:
                    return value
            if self._stat_key in ("difficulty", "verificationprogress"):
                try:
                    return float(value)
                except Exception:
                    return value
            if self._stat_key in ("initialblockdownload", "pruned"):
                return bool(value)
            if self._stat_key == "warnings":
                return ", ".join(value) if isinstance(value, list) else value
            return value
        return None

    @property
    def available(self):
        data = self.coordinator.data.get("blockchaininfo")
        return data is not None and self._stat_key in data

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "bitcoin_explorer")},
            "name": "Bitcoin Explorer",
            "manufacturer": "Sovereign Bitcoin Node",
            "model": "Bitcoin Explorer API",
        }


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    sensors = [
        BitcoinNextHalvingSensor(coordinator),
        BitcoinBlockTipSensor(coordinator),
        BitcoinCurrentBlockHeaderSensor(coordinator),
    ]
    # Add a SoloPoolStatSensor for each stat
    for stat_key, icon in MINING_POOL_STATS:
        sensors.append(SoloPoolStatSensor(coordinator, stat_key, icon))
    # Add a BitcoinExplorerStatSensor for each blockchaininfo stat
    for stat_key, icon in BITCOIN_EXPLORER_STATS:
        sensors.append(BitcoinExplorerStatSensor(coordinator, stat_key, icon))
    # Add a BitcoinExplorerIndexStatSensor for each getindexinfo stat
    for stat_key, icon in BITCOIN_EXPLORER_INDEX_STATS:
        sensors.append(BitcoinExplorerIndexStatSensor(coordinator, stat_key, icon))
    # Add Mempool sensors
    for stat_key, icon in MEMPOOL_STATS:
        sensors.append(MempoolFeeSensor(coordinator, stat_key, icon))
    # Add Mempool price sensors
    for stat_key, icon in MEMPOOL_PRICE_STATS:
        sensors.append(MempoolPriceSensor(coordinator, stat_key, icon))
    # Add Bitcoind sensors
    sensors.append(BitcoindSyncStateSensor(coordinator))
    sensors.append(BitcoindSyncPercentSensor(coordinator))
    sensors.append(BitcoindPeersIncomingSensor(coordinator))
    sensors.append(BitcoindPeersOutgoingSensor(coordinator))
    sensors.append(BitcoindBlocksSyncedSensor(coordinator))
    sensors.append(BitcoindVersionSensor(coordinator))
    sensors.append(BitcoindUptimeSensor(coordinator))
    async_add_entities(sensors)


# Bitcoind uptime sensor
class BitcoindUptimeSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "Bitcoind Node Uptime"
    _attr_unique_id = "bitcoind_uptime"
    _attr_device_class = "timestamp"
    _attr_icon = "mdi:clock-start"

    @property
    def native_value(self):
        ts = self.coordinator.data.get("bitcoind_uptime")
        if ts:
            import datetime
            return datetime.datetime.utcfromtimestamp(ts).replace(tzinfo=datetime.timezone.utc)
        return None

    @property
    def available(self):
        return self.coordinator.data.get("bitcoind_uptime") is not None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "bitcoind")},
            "name": "Bitcoind",
            "manufacturer": "Bitcoin Core",
            "model": "bitcoind RPC",
        }


class BitcoindSyncStateSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "Blockchain Initial Sync"
    _attr_unique_id = "blockchain_initial_sync"
    _attr_icon = "mdi:sync"

    @property
    def native_value(self):
        data = self.coordinator.data.get("bitcoind_sync_state")
        if data is not None:
            # Return the IBD (initialblockdownload) state if present, else None
            return data.get("initialblockdownload")
        return None

    @property
    def available(self):
        data = self.coordinator.data.get("bitcoind_sync_state")
        return data is not None and "initialblockdownload" in data


    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "bitcoind")},
            "name": "Bitcoind",
            "manufacturer": "Bitcoin Core",
            "model": "bitcoind RPC",
        }


# The following must be outside the class!
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    sensors = [
        BitcoinNextHalvingSensor(coordinator),
        BitcoinBlockTipSensor(coordinator),
        BitcoinCurrentBlockHeaderSensor(coordinator),
    ]
    # Add a SoloPoolStatSensor for each stat
    for stat_key, icon in MINING_POOL_STATS:
        sensors.append(SoloPoolStatSensor(coordinator, stat_key, icon))
    # Add a BitcoinExplorerStatSensor for each blockchaininfo stat
    for stat_key, icon in BITCOIN_EXPLORER_STATS:
        sensors.append(BitcoinExplorerStatSensor(coordinator, stat_key, icon))
    # Add a BitcoinExplorerIndexStatSensor for each getindexinfo stat
    for stat_key, icon in BITCOIN_EXPLORER_INDEX_STATS:
        sensors.append(BitcoinExplorerIndexStatSensor(coordinator, stat_key, icon))
    # Add Mempool sensors
    for stat_key, icon in MEMPOOL_STATS:
        sensors.append(MempoolFeeSensor(coordinator, stat_key, icon))
    # Add Mempool price sensors
    for stat_key, icon in MEMPOOL_PRICE_STATS:
        sensors.append(MempoolPriceSensor(coordinator, stat_key, icon))
    # Add Bitcoind sync state sensor
    sensors.append(BitcoindSyncStateSensor(coordinator))
    sensors.append(BitcoindSyncPercentSensor(coordinator))
    sensors.append(BitcoindPeersIncomingSensor(coordinator))
    sensors.append(BitcoindPeersOutgoingSensor(coordinator))
    sensors.append(BitcoindBlocksSyncedSensor(coordinator))
    sensors.append(BitcoindVersionSensor(coordinator))
    async_add_entities(sensors)


# Bitcoind sync percent sensor
class BitcoindSyncPercentSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "Bitcoind Sync Progress %"
    _attr_unique_id = "bitcoind_sync_percent"
    _attr_icon = "mdi:progress-clock"

    @property
    def native_value(self):
        val = self.coordinator.data.get("bitcoind_sync_progress")
        if val is not None:
            # Clamp to 0-100 and return as int
            pct = int(round(float(val) * 100))
            return max(0, min(pct, 100))
        return None

    @property
    def available(self):
        return self.coordinator.data.get("bitcoind_sync_progress") is not None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "bitcoind")},
            "name": "Bitcoind",
            "manufacturer": "Bitcoin Core",
            "model": "bitcoind RPC",
        }

# Bitcoind peers incoming sensor
class BitcoindPeersIncomingSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "Bitcoind Peers Incoming"
    _attr_unique_id = "bitcoind_peers_incoming"
    _attr_icon = "mdi:arrow-down-bold"

    @property
    def native_value(self):
        return self.coordinator.data.get("bitcoind_peers_incoming")

    @property
    def available(self):
        return self.coordinator.data.get("bitcoind_peers_incoming") is not None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "bitcoind")},
            "name": "Bitcoind",
            "manufacturer": "Bitcoin Core",
            "model": "bitcoind RPC",
        }

# Bitcoind peers outgoing sensor
class BitcoindPeersOutgoingSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "Bitcoind Peers Outgoing"
    _attr_unique_id = "bitcoind_peers_outgoing"
    _attr_icon = "mdi:arrow-up-bold"

    @property
    def native_value(self):
        return self.coordinator.data.get("bitcoind_peers_outgoing")

    @property
    def available(self):
        return self.coordinator.data.get("bitcoind_peers_outgoing") is not None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "bitcoind")},
            "name": "Bitcoind",
            "manufacturer": "Bitcoin Core",
            "model": "bitcoind RPC",
        }

# Bitcoind blocks synced sensor
class BitcoindBlocksSyncedSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "Bitcoind Blocks Synced"
    _attr_unique_id = "bitcoind_blocks_synced"
    _attr_icon = "mdi:counter"

    @property
    def native_value(self):
        blocks = self.coordinator.data.get("bitcoind_blocks")
        headers = self.coordinator.data.get("bitcoind_headers")
        if blocks is not None and headers is not None:
            return f"{blocks:06}/{headers:06}"
        return None

    @property
    def available(self):
        return self.coordinator.data.get("bitcoind_blocks") is not None and self.coordinator.data.get("bitcoind_headers") is not None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "bitcoind")},
            "name": "Bitcoind",
            "manufacturer": "Bitcoin Core",
            "model": "bitcoind RPC",
        }

# Bitcoind version sensor
class BitcoindVersionSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "Bitcoind Version"
    _attr_unique_id = "bitcoind_version"
    _attr_icon = "mdi:information-outline"

    @property
    def native_value(self):
        return self.coordinator.data.get("bitcoind_version")

    @property
    def available(self):
        return self.coordinator.data.get("bitcoind_version") is not None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "bitcoind")},
            "name": "Bitcoind",
            "manufacturer": "Bitcoin Core",
            "model": "bitcoind RPC",
        }


import datetime


class BitcoinNextHalvingSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "Bitcoin Next Halving"
    _attr_unique_id = "btc_halving_rest_source"
    _attr_device_class = "timestamp"
    _attr_icon = "mdi:calendar-clock"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "bitcoin_explorer")},
            "name": "Bitcoin Explorer",
            "manufacturer": "Sovereign Bitcoin Node",
            "model": "Bitcoin Explorer API",
        }


    @property
    def native_value(self):
        data = self.coordinator.data.get("next_halving")
        if data:
            date_str = data.get("nextHalvingEstimatedDate")
            if date_str:
                try:
                    return datetime.datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                except Exception:
                    return None
        return None

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data.get("next_halving")
        if not data:
            return None
        attrs = {
            "nextHalvingIndex": data.get("nextHalvingIndex"),
            "nextHalvingBlock": data.get("nextHalvingBlock"),
            "nextHalvingSubsidy": data.get("nextHalvingSubsidy"),
            "blocksUntilNextHalving": data.get("blocksUntilNextHalving"),
            "timeUntilNextHalving": data.get("timeUntilNextHalving"),
            "nextHalvingEstimatedDate": data.get("nextHalvingEstimatedDate"),
        }
        # Add human readable time remaining
        date_str = data.get("nextHalvingEstimatedDate")
        if date_str:
            try:
                target = datetime.datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                now = datetime.datetime.now(target.tzinfo)
                delta = target - now
                years, remainder = divmod(delta.days, 365)
                months, days = divmod(remainder, 30)
                attrs["time_until_halving_human"] = f"{years}y {months}m {days}d"
            except Exception:
                attrs["time_until_halving_human"] = None
        return attrs

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data.get("next_halving")
        if not data:
            return None
        return {
            "nextHalvingIndex": data.get("nextHalvingIndex"),
            "nextHalvingBlock": data.get("nextHalvingBlock"),
            "nextHalvingSubsidy": data.get("nextHalvingSubsidy"),
            "blocksUntilNextHalving": data.get("blocksUntilNextHalving"),
            "timeUntilNextHalving": data.get("timeUntilNextHalving"),
            "nextHalvingEstimatedDate": data.get("nextHalvingEstimatedDate"),
        }


class BitcoinBlockTipSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "Bitcoin Block Tip"
    _attr_unique_id = "btc_block_tip"
    _attr_icon = "mdi:cube-outline"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "bitcoin_explorer")},
            "name": "Bitcoin Explorer",
            "manufacturer": "Sovereign Bitcoin Node",
            "model": "Bitcoin Explorer API",
        }

    @property
    def native_value(self):
        data = self.coordinator.data.get("block_tip")
        if data:
            return data.get("height")
        return None

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data.get("block_tip")
        if not data:
            return None
        return {
            "height": data.get("height"),
            "hash": data.get("hash"),
        }


class BitcoinCurrentBlockHeaderSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "Bitcoin Current Block Header"
    _attr_unique_id = "btc_current_block_header"
    _attr_icon = "mdi:code-braces"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "bitcoin_explorer")},
            "name": "Bitcoin Explorer",
            "manufacturer": "Sovereign Bitcoin Node",
            "model": "Bitcoin Explorer API",
        }

    @property
    def native_value(self):
        data = self.coordinator.data.get("current_block_header")
        if data:
            return data.get("hash")
        return None

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data.get("current_block_header")
        if not data:
            return None
        return {
            "hash": data.get("hash"),
            "confirmations": data.get("confirmations"),
            "height": data.get("height"),
            "version": data.get("version"),
            "versionHex": data.get("versionHex"),
            "merkleroot": data.get("merkleroot"),
            "time": data.get("time"),
            "mediantime": data.get("mediantime"),
            "nonce": data.get("nonce"),
            "bits": data.get("bits"),
            "target": data.get("target"),
            "difficulty": data.get("difficulty"),
            "chainwork": data.get("chainwork"),
            "nTx": data.get("nTx"),
            "previousblockhash": data.get("previousblockhash"),
            "nextblockhash": data.get("nextblockhash"),
        }
