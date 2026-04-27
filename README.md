# Sovereign Bitcoin Node Manager

A Home Assistant custom integration for monitoring and managing a Sovereign Bitcoin Node.

## Features
- Device and sensor entities for:
  - Bitcoin Explorer
  - Bitcoind (RPC)
  - Mempool
  - Solo Pool
- Bitcoin Next Halving sensor with human-readable countdown


## Installation
1. Copy the `sovereign_bitcoin_mgmt` folder to your Home Assistant `custom_components` directory.
2. Restart Home Assistant.
3. Add the integration via the UI.

## Configuration
- Use the Home Assistant UI config flow to set up your node details.
- All required fields are prompted during setup.


## Adding to Home Assistant via HACS

To add this custom integration to Home Assistant using HACS:

1. Go to **HACS** in your Home Assistant sidebar.
2. Click the three dots menu (⋮) in the top right and select **Custom repositories**.
3. Enter this repository URL: `https://github.com/daylehouse/Sovereign-Bitcoin-Node-Manager`
4. Set the category to **Integration** and click **Add**.
5. Find "Sovereign Bitcoin Node Manager" in HACS Integrations and install.
6. Restart Home Assistant.
7. Add the integration via the UI.

## Development
- See the code for advanced customization and sensor details.

## License
MIT
