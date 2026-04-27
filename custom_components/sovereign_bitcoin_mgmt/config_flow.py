import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN



CONF_BTC_ADDRESSES = "btc_addresses"
CONF_BITCOIND_PORT = "bitcoind_port"
CONF_BITCOIND_RPC_USER = "bitcoind_rpc_user"
CONF_BITCOIND_RPC_PASSWORD = "bitcoind_rpc_password"
CONF_BITCOIN_EXPLORER_PORT = "bitcoin_explorer_port"
CONF_MEMPOOL_PORT = "mempool_port"
CONF_PUBLIC_POOL_PORT = "public_pool_port"
CONF_RTL_PORT = "rtl_port"

class SovereignBitcoinConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_HOST], data=user_input)
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Optional(CONF_BITCOIND_PORT, default=8332): int,
                vol.Optional(CONF_BITCOIND_RPC_USER): str,
                vol.Optional(CONF_BITCOIND_RPC_PASSWORD): str,
                vol.Optional(CONF_BTC_ADDRESSES): str,
                vol.Optional(CONF_BITCOIN_EXPLORER_PORT, default=3020): int,
                vol.Optional(CONF_MEMPOOL_PORT, default=4080): int,
                vol.Optional(CONF_PUBLIC_POOL_PORT, default=3334): int,
                vol.Optional(CONF_RTL_PORT, default=3000): int,
            }),
            errors=errors,
            description_placeholders={"icon": "/local/community/sovereign_bitcoin_mgmt/brand/icon.png"},
        )
