"""EF-PowerOcean-TcpModbus – Local Modbus TCP integration for EcoFlow PowerOcean Plus."""

from __future__ import annotations

import logging

from homeassistant.const import Platform
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN
from .coordinator import EcoflowCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
]
CONFIG_VERSION = 2

# Die Register 40580-40594 liegen auf der Wechselrichter-Seite, wurden aber als
# Netz-Werte benannt. Beim Umbenennen der Keys ändert sich die unique_id, daher
# werden die bestehenden Entities migriert, damit die Historie erhalten bleibt.
RENAMED_ENTITY_KEYS = {
    "voltage_l1": "inverter_voltage_l1",
    "voltage_l2": "inverter_voltage_l2",
    "voltage_l3": "inverter_voltage_l3",
    "current_l1": "inverter_current_l1",
    "current_l2": "inverter_current_l2",
    "current_l3": "inverter_current_l3",
    "frequency": "inverter_frequency",
}


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old config entries to current schema."""

    if config_entry.version >= CONFIG_VERSION:
        return True

    _LOGGER.info(
        f"Migrating config entry {config_entry.entry_id} from version {config_entry.version} to {CONFIG_VERSION}."
    )

    registry = er.async_get(hass)
    for entry in er.async_entries_for_config_entry(registry, config_entry.entry_id):
        prefix = f"{config_entry.entry_id}_"
        if not entry.unique_id.startswith(prefix):
            continue
        old_key = entry.unique_id[len(prefix) :]
        new_key = RENAMED_ENTITY_KEYS.get(old_key)
        if new_key is None:
            continue

        new_unique_id = f"{prefix}{new_key}"
        if registry.async_get_entity_id(entry.domain, DOMAIN, new_unique_id):
            _LOGGER.warning(
                f"Can not migrate '{entry.entity_id}' to '{new_key}' – target unique_id already exists."
            )
            continue

        _LOGGER.debug(
            f"Migrating unique_id of '{entry.entity_id}': {old_key} -> {new_key}"
        )
        registry.async_update_entity(entry.entity_id, new_unique_id=new_unique_id)

    hass.config_entries.async_update_entry(config_entry, version=CONFIG_VERSION)
    _LOGGER.info(
        f"Migration of config entry {config_entry.entry_id} to version {CONFIG_VERSION} successful!"
    )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up EF-PowerOcean-TcpModbus from a config entry."""

    coordinator = EcoflowCoordinator(
        hass,
        config_entry=entry,
    )
    await coordinator.async_connect_client()
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Reload integration when config entry data changes
    entry.async_on_unload(entry.add_update_listener(_async_reload_entry))

    return True


async def _async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload the integration when the config entry is updated."""
    _LOGGER.debug("Config entry updated — reloading EF-PowerOcean-TcpModbus")
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if not unload_ok:
        return False

    # close connection and shutdown
    coordinator: EcoflowCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
    await coordinator.async_client_shutdown()

    return True
