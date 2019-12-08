from cozypy.utils import TextEnum

COZYTOUCH_BASE_URL = "https://ha110-1.overkiz.com/enduser-mobile-web/enduserAPI"

COZYTOUCH_ENDPOINTS = {
    "login": "{base_url}/login".format(base_url=COZYTOUCH_BASE_URL),
    "setup": "{base_url}/setup".format(base_url=COZYTOUCH_BASE_URL),
    "devices": "{base_url}/setup/devices".format(base_url=COZYTOUCH_BASE_URL),
    "deviceInfo": "{base_url}/setup/devices/[device_url]/states".format(base_url=COZYTOUCH_BASE_URL),
    "stateInfo": "{base_url}/setup/devices/[device_url]/states/[state_name]".format(base_url=COZYTOUCH_BASE_URL),
    "apply": "{base_url}/exec/apply".format(base_url=COZYTOUCH_BASE_URL)
}

USER_AGENT = "Home assistant/Cozytouch"

class DeviceType(TextEnum):
    POD = "Pod"
    HEATER = "AtlanticElectricalHeaterWithAdjustableTemperatureSetpoint"
    HEATER_PASV = "AtlanticElectricalHeater"
    WATER_HEATER = "DomesticHotWaterProduction"
    TEMPERATURE = "TemperatureSensor"
    CONTACT = "ContactSensor"
    OCCUPANCY = "OccupancySensor"
    ELECTRECITY = "CumulativeElectricPowerConsumptionSensor"


class DeviceState(TextEnum):
    MANUFACTURER_NAME_STATE = 'core:ManufacturerNameState'
    WH_CAPACITY_STATE = 'io:DHWCapacityState'
    AWAY_STATE = 'core:HolidaysModeState'
    WH_MODE_STATE = 'io:DHWModeState'
    WH_AWAY_STATE = 'io:DHWAbsenceModeState'
    WH_AWAY_MODE_DURATION_STATE = 'io:AwayModeDurationState'
    WH_BOOST_STATE = 'io:DHWBoostModeState'
    WH_BOOST_MODE_DURATION_STATE = 'core:BoostModeDurationState'   
    WH_SHOWER_REMAINING_STATE = 'core:NumberOfShowerRemainingState'
    WH_SHOWER_CAPACITY_STATE = 'core:ExpectedNumberOfShowerState'
    WH_HEATING_STATUS_STATE = 'core:HeatingStatusState'
    WH_STATUS_STATE = 'core:StatusState'
    WH_TANK_STATE = 'core:NumberOfTankState'
    WH_WATER_VOLUME_ESTIMATION_STATE = 'core:V40WaterVolumeEstimationState'
    WH_MIDDLE_W_TEMPERATURE_STATE = 'io:MiddleWaterTemperatureState'
    WH_ERROR_STATE = 'io:DHWErrorState'
    ANTI_LEGIONELLOSIS_STATE = 'io:AntiLegionellosisState'
    OPERATING_RANGE_STATE = 'io:OperatingRangeState'
    OPERATING_MODE_CAPABILITIES_STATE = 'io:OperatingModeCapabilitiesState'
    OPERATING_MODE_STATE = 'core:OperatingModeState'
    TARGETING_HEATING_LEVEL_STATE = 'io:TargetHeatingLevelState'
    OCCUPANCY_STATE = "core:OccupancyState"
    TEMPERATURE_STATE = "core:TemperatureState"
    COMFORT_TEMPERATURE_STATE = "core:ComfortRoomTemperatureState"
    ECO_TEMPERATURE_STATE = "core:EcoRoomTemperatureState"
    TARGET_TEMPERATURE_STATE = "core:TargetTemperatureState"
    ON_OFF_STATE = "core:OnOffState"
    ELECTRIC_ENERGY_CONSUMPTION_STATE = "core:ElectricEnergyConsumptionState"
    POWER_HEAT_ELECTRICAL_STATE = "io:PowerHeatElectricalState"
    POWER_HEAT_PUMP_STATE = "io:PowerHeatPumpState"
    HEAT_PUMP_OPERATING_TIME_STATE = 'io:HeatPumpOperatingTimeState'
    ELECTRIC_BOOSTER_OPERATING_TIME_STATE = 'io:ElectricBoosterOperatingTimeState'


class OnOffState(TextEnum):
    ON = "on"
    OFF = "off"


class AwayModeState(TextEnum):
    ON = "on"
    OFF = "off"


class OperatingModeState(TextEnum):
    STANDBY = "standby"
    BASIC = "basic"
    INTERNAL = "internal"
    AUTO = "auto"


class TargetingHeatingLevelState(TextEnum):
    ECO = "eco"
    BOOST = "boost"
    COMFORT = "comfort"
    COMFORT_ONE = "comfort-1"
    COMFORT_TWO = "comfort-2"
    FROST_PROTECTION = "frostprotection"
    SECURED = "secured"
    OFF = "off"


class DeviceCommand(TextEnum):
    SET_OPERATION_MODE = "setOperatingMode"
    SET_HEATING_LEVEL = "setHeatingLevel"
    SET_ECO_TEMP = "setEcoTemperature"
    SET_LOWERING_TEMP_PROG = "setSetpointLoweringTemperatureInProgMode"
    SET_COMFORT_TEMP = "setComfortTemperature"
    SET_AWAY_MODE = "setHolidays"
    SET_TARGET_TEMP = "setTargetTemperature"

    REFRESH_OPERATION_MODE = "refreshOperatingMode"
    REFRESH_ECO_TEMPERATURE = "refreshEcoTemperature"
    REFRESH_COMFORT_TEMPERATURE = "refreshComfortTemperature"
    REFRESH_HEATING_LEVEL = "refreshHeatingLevel"
    REFRESH_TARGET_TEMPERATURE = "refreshTargetTemperature"
    REFRESH_LOWERING_TEMP_PROG = "refreshSetpointLoweringTemperatureInProgMode"
