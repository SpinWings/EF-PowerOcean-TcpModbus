"""Constants for EF-PowerOcean-TcpModbus integration."""

from __future__ import annotations

from dataclasses import dataclass

DOMAIN = "ef_powerocean_tcpmodbus"
DEFAULT_PORT = 502
DEFAULT_SLAVE = 1
DEFAULT_SCAN_INTERVAL = 5  # seconds
DEFAULT_BATTERY_COUNT = 0
DEFAULT_MAX_SOLAR_POWER = 12000
DEFAULT_MAX_GRID_POWER = 15000
DEFAULT_MAX_POWER = 30000

CONF_HOST = "host"
CONF_PORT = "port"
CONF_BATTERY_COUNT = "battery_count"
CONF_MAX_SOLAR_POWER = "solar_power_max"
CONF_MAX_GRID_POWER = "grid_power_max"
CONF_MAX_BATTERY_CHARGED_POWER = "battery_charged_power_max"
CONF_MAX_BATTERY_DISCHARGED_POWER = "battery_discharged_power_max"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_CALC_SOLAR_POWER = "calc_solar_power"

PV_VOLTAGE_THRESHOLD = 250
MAX_BATTERY_CHARGED_POWER = 2500
MAX_BATTERY_DISCHARGED_POWER = 3300


@dataclass(frozen=True)
class RegisterDef:
    key: str
    block_index: int
    size: int = 2


@dataclass(frozen=True)
class BlockDef:
    start_register: int
    content: list[RegisterDef]
    num_read_regs: int = 100


@dataclass(frozen=True)
class SensorDef:
    key: str
    name: str | None = None
    unit: str | None = None
    device_class: str | None = None
    state_class: str | None = None
    entity_category: str | None = None


@dataclass(frozen=True)
class EnergySensorDef:
    key: str
    name: str | None = None
    unit: str = "kWh"
    reset_at_midnight: bool = False  # nur bei Sensor die aus einem Register gelesen werden, keine berechneten Sensoren
    is_calculated: bool = False
    max_power: int | None = None
    device_class: str = "energy"
    state_class: str = "total_increasing"
    entity_category: str | None = None


@dataclass(frozen=True)
class BinarySensorDef:
    key: str
    name: str | None = None
    device_class: str | None = None
    entity_category: str | None = None


MOD_REGISTER_MAP = {
    "serial_number": 40004,
    "blocks": [
 #       BlockDef(
 #           start_register=40004,
 #           num_read_regs=12,
 #           content=[
 #               RegisterDef(key="operation_mode", block_index=9, size=1),
 #           ],
 #       ),
        BlockDef(
            start_register=40519,
            content=[
                RegisterDef(key="house_power", block_index=0),                          # 40519 ✅
                RegisterDef(key="grid_power", block_index=2),                           # 40521 ✅
                RegisterDef(key="solar_power", block_index=4),                          # 40523 ✅
                RegisterDef(key="battery_power", block_index=6),                        # 40525 ✅
                RegisterDef(key="battery_soc", block_index=8, size=1),                  # 40527 ✅
                RegisterDef(key="system_modes", block_index=11, size=1),                # 40530 ✅
                RegisterDef(key="min_soc_limit", block_index=17, size=1),               # 40536 ✅  
                # RegisterDef(key="bat_temp_warn_max", block_index=21, size=1),
                RegisterDef(key="status_leds_brightness", block_index=22, size=1),      # 40541 ✅
                #RegisterDef(key="limit_inv_power", block_index=27, size=1),
                #RegisterDef(key="limit_inv_max", block_index=29, size=1),
                #RegisterDef(key="battery_capacity", block_index=33, size=1),
                # 40559-40569: Netz-Seite (Grid)
                RegisterDef(key="grid_current_l1", block_index=40),                     # 40559 ✅
                RegisterDef(key="grid_current_l2", block_index=42),                     # 40561 ✅
                RegisterDef(key="grid_current_l3", block_index=44),                     # 40563 ✅
                RegisterDef(key="grid_voltage_l1", block_index=46),                     # 40565 ✅
                RegisterDef(key="grid_voltage_l2", block_index=48),                     # 40567 ✅
                RegisterDef(key="grid_voltage_l3", block_index=50),                     # 40569 ✅      
                RegisterDef(key="battery_voltage", block_index=55),                     # 40574 ✅
                RegisterDef(key="battery_current", block_index=57),                     # 40576 ✅
                RegisterDef(key="battery_temperature", block_index=59),                 # 40578 ✅  
                # 40580-40594 liegen auf der Wechselrichter-Seite, nicht am Netz
                RegisterDef(key="inverter_voltage_l1", block_index=61),                 # 40580 ✅ formerly voltage_l1
                RegisterDef(key="inverter_voltage_l2", block_index=63),                 # 40582 ✅ formerly voltage_l2
                RegisterDef(key="inverter_voltage_l3", block_index=65),                 # 40584 ✅ formerly voltage_l3
                RegisterDef(key="inverter_current_l1", block_index=67),                 # 40586 ✅ formerly current_l1
                RegisterDef(key="inverter_current_l2", block_index=69),                 # 40588 ✅ formerly current_l2
                RegisterDef(key="inverter_current_l3", block_index=71),                 # 40590 ✅ formerly current_l3 
                RegisterDef(key="inverter_temperature", block_index=73),                # 40592 ✅
                RegisterDef(key="inverter_frequency", block_index=75),                  # 40594 ✅
                RegisterDef(key="pv1_voltage", block_index=77),                         # 40596 ✅
                RegisterDef(key="pv2_voltage", block_index=79),                         # 40598 ✅
                RegisterDef(key="pv3_voltage", block_index=81),                         # 40600 ✅
                RegisterDef(key="pv1_current", block_index=83),                         # 40602 ✅  
                RegisterDef(key="pv2_current", block_index=85),                         # 40604 ✅
                RegisterDef(key="pv3_current", block_index=87),                         # 40606 
                #RegisterDef(key="feed_in_power_max", block_index=90, size=1),
            ],
        ),
        BlockDef(
            start_register=42081,
            num_read_regs=4,
            content=[
                RegisterDef(key="battery_module_count", block_index=0, size=1),         # 42081 ✅
                RegisterDef(key="soc_battery_1", block_index=1, size=1),                # 42082 ✅
                RegisterDef(key="soc_battery_2", block_index=2, size=1),                # 42083 ✅
                RegisterDef(key="soc_battery_3", block_index=3, size=1),                # 42084 
            ],
        ),
        BlockDef(
            start_register=42161,
            content=[
                RegisterDef(key="grid_import_total", block_index=0),                    # 42161 ✅  
                RegisterDef(key="grid_import_today", block_index=2),                    # 42163 ✅
                RegisterDef(key="grid_export_total", block_index=16),                   # 42177 ✅
                RegisterDef(key="grid_export_today", block_index=18),                   # 42179 ✅
                RegisterDef(key="bat_charged_total", block_index=64),                   # 42225 ✅
                RegisterDef(key="bat_charged_today", block_index=66),                   # 42227 ✅
                RegisterDef(key="bat_discharged_total", block_index=80),                # 42241 ✅     
                RegisterDef(key="bat_discharged_today", block_index=82),                # 42243 ✅    
                RegisterDef(key="solar_total", block_index=96),                         # 42257 ✅
                RegisterDef(key="solar_today", block_index=98),                         # 42259 ✅
            ],
        ),
    ],
}


SENSOR_MAP: list[SensorDef] = [
    SensorDef(
        key="serial_number",
        unit=None,
        device_class=None,
        state_class=None,
        entity_category="diagnostic",
    ),
#    SensorDef(
#        key="operation_mode",
#        unit=None,
#        device_class=None,
#        state_class="measurement",
#        entity_category="diagnostic",
#   ),
    SensorDef(
        key="system_modes",
        unit=None,
        device_class=None,
        state_class="measurement",
    ),
    SensorDef(
        key="house_power",
        unit="W",
        device_class="power",
        state_class="measurement",
    ),
    SensorDef(
        key="grid_power",
        unit="W",
        device_class="power",
        state_class="measurement",
    ),
    SensorDef(
        key="solar_power",
        unit="W",
        device_class="power",
        state_class="measurement",
    ),
    SensorDef(
        key="battery_power",
        unit="W",
        device_class="power",
        state_class="measurement",
    ),
    SensorDef(
        key="battery_soc",
        unit="%",
        device_class="battery",
        state_class="measurement",
    ),
    SensorDef(
        key="min_soc_limit",
        unit="%",
        device_class="battery",
        state_class="measurement",
    ),
    # SensorDef(
    #     key="bat_temp_warn_max",
    #     unit="°C",
    #     device_class="temperature",
    #     state_class="measurement",
    #     entity_category="diagnostic",
    # ),
    SensorDef(
        key="status_leds_brightness",
        unit="%",
        device_class=None,
        state_class="measurement",
        entity_category="diagnostic",
    ),
    # SensorDef(
    #     key="limit_inv_power",
    #     unit="W",
    #     device_class="power",
    #     state_class="measurement",
    #     entity_category="diagnostic",
    # ),
    # SensorDef(
    #     key="limit_inv_max",
    #     unit="W",
    #     device_class="power",
    #     state_class="measurement",
    #     entity_category="diagnostic",
    # ),
    SensorDef(
        key="limit_charge",
        unit="W",
        device_class="power",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="limit_discharge",
        unit="W",
        device_class="power",
        state_class="measurement",
        entity_category="diagnostic",
    ),
#    SensorDef(
#       key="battery_capacity",
#        unit="Wh",
#        device_class="storage",
#        state_class="measurement",
#        entity_category="diagnostic",
#    ),
    SensorDef(
        key="battery_voltage",
        unit="V",
        device_class="voltage",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="battery_current",
        unit="A",
        device_class="current",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="battery_temperature",
        unit="°C",
        device_class="temperature",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="grid_voltage_l1",
        unit="V",
        device_class="voltage",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="grid_voltage_l2",
        unit="V",
        device_class="voltage",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="grid_voltage_l3",
        unit="V",
        device_class="voltage",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="grid_current_l1",
        unit="A",
        device_class="current",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="grid_current_l2",
        unit="A",
        device_class="current",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="grid_current_l3",
        unit="A",
        device_class="current",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="grid_apparentpower_l1",
        unit="VA",
        device_class="apparent_power",
        state_class="measurement",
    ),
    SensorDef(
        key="grid_apparentpower_l2",
        unit="VA",
        device_class="apparent_power",
        state_class="measurement",
    ),
    SensorDef(
        key="grid_apparentpower_l3",
        unit="VA",
        device_class="apparent_power",
        state_class="measurement",
    ),
    SensorDef(
        key="grid_apparentpower",
        unit="VA",
        device_class="apparent_power",
        state_class="measurement",
    ),
    SensorDef(
        key="inverter_voltage_l1",
        unit="V",
        device_class="voltage",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="inverter_voltage_l2",
        unit="V",
        device_class="voltage",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="inverter_voltage_l3",
        unit="V",
        device_class="voltage",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="inverter_current_l1",
        unit="A",
        device_class="current",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="inverter_current_l2",
        unit="A",
        device_class="current",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="inverter_current_l3",
        unit="A",
        device_class="current",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="inverter_apparentpower_l1",
        unit="VA",
        device_class="apparent_power",
        state_class="measurement",
    ),
    SensorDef(
        key="inverter_apparentpower_l2",
        unit="VA",
        device_class="apparent_power",
        state_class="measurement",
    ),
    SensorDef(
        key="inverter_apparentpower_l3",
        unit="VA",
        device_class="apparent_power",
        state_class="measurement",
    ),
    SensorDef(
        key="inverter_apparentpower",
        unit="VA",
        device_class="apparent_power",
        state_class="measurement",
    ),
    SensorDef(
        key="inverter_temperature",
        unit="°C",
        device_class="temperature",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="inverter_frequency",
        unit="Hz",
        device_class="frequency",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="pv1_voltage",
        unit="V",
        device_class="voltage",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="pv2_voltage",
        unit="V",
        device_class="voltage",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="pv3_voltage",
        unit="V",
        device_class="voltage",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="pv1_current",
        unit="A",
        device_class="current",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="pv2_current",
        unit="A",
        device_class="current",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="pv3_current",
        unit="A",
        device_class="current",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    # SensorDef(
    #     key="feed_in_power_max",
    #     unit="W",
    #     device_class="power",
    #     state_class="measurement",
    #     entity_category="diagnostic",
    # ),
    SensorDef(
        key="battery_module_count",
        unit=None,
        device_class=None,
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="soc_battery_1",
        unit="%",
        device_class="battery",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="soc_battery_2",
        unit="%",
        device_class="battery",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="soc_battery_3",
        unit="%",
        device_class="battery",
        state_class="measurement",
        entity_category="diagnostic",
    ),
    SensorDef(
        key="bat_remaining",
        unit="kWh",
        device_class="energy_storage",
        state_class="measurement",
    ),
    SensorDef(
        key="pv1_power",
        unit="W",
        device_class="power",
        state_class="measurement",
    ),
    SensorDef(
        key="pv2_power",
        unit="W",
        device_class="power",
        state_class="measurement",
    ),
    SensorDef(
        key="pv3_power",
        unit="W",
        device_class="power",
        state_class="measurement",
    ),
    SensorDef(
        key="bat_net_energy",
        unit="kWh",
        device_class="energy",
        state_class="total",
    ),
]


ENERGY_SENSOR_MAP: list[EnergySensorDef] = [
    EnergySensorDef("grid_import_total", max_power=CONF_MAX_GRID_POWER),
    EnergySensorDef(
        "grid_import_today", reset_at_midnight=True, max_power=CONF_MAX_GRID_POWER
    ),
    EnergySensorDef("grid_export_total", max_power=CONF_MAX_SOLAR_POWER),
    EnergySensorDef(
        "grid_export_today", reset_at_midnight=True, max_power=CONF_MAX_SOLAR_POWER
    ),
    EnergySensorDef("bat_charged_total", max_power=CONF_MAX_BATTERY_CHARGED_POWER),
    EnergySensorDef(
        "bat_charged_today",
        reset_at_midnight=True,
        max_power=CONF_MAX_BATTERY_CHARGED_POWER,
    ),
    EnergySensorDef(
        "bat_discharged_total", max_power=CONF_MAX_BATTERY_DISCHARGED_POWER
    ),
    EnergySensorDef(
        "bat_discharged_today",
        reset_at_midnight=True,
        max_power=CONF_MAX_BATTERY_DISCHARGED_POWER,
    ),
    EnergySensorDef("solar_total", max_power=CONF_MAX_SOLAR_POWER),
    EnergySensorDef(
        "solar_today", reset_at_midnight=True, max_power=CONF_MAX_SOLAR_POWER
    ),
    EnergySensorDef(
        "house_energy_today",
        is_calculated=True,
        max_power=CONF_MAX_GRID_POWER,
    ),
    EnergySensorDef(
        "house_energy_total",
        is_calculated=True,
        max_power=CONF_MAX_GRID_POWER,
    ),
]


BINARY_SENSOR_MAP: list[BinarySensorDef] = [
    BinarySensorDef("island_mode", "grid"),
    BinarySensorDef("self_use_mode_ena", "battery"),
    BinarySensorDef("intelligent_mode_ena", "battery"),
    BinarySensorDef("battery_saver_mode_ena", "battery"),
]
