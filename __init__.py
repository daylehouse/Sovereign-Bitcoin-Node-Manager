
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN
from .coordinator import SovereignBitcoinCoordinator

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    config = entry.data
    coordinator = SovereignBitcoinCoordinator(
        hass,
        host=config.get("host"),
        btc_addresses=config.get("btc_addresses"),
        public_pool_port=config.get("public_pool_port", 3334),
        bitcoind_port=config.get("bitcoind_port", 8332),
        bitcoind_rpc_user=config.get("bitcoind_rpc_user"),
        bitcoind_rpc_password=config.get("bitcoind_rpc_password"),
    )
    await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN][entry.entry_id] = {"coordinator": coordinator}

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")
