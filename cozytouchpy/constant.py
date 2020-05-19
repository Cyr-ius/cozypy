"""Constants."""

from .utils import TextEnum

COZYTOUCH_BASE_URL = "https://ha110-1.overkiz.com/enduser-mobile-web/enduserAPI"

COZYTOUCH_ENDPOINTS = {
    "login": "{base_url}/login".format(base_url=COZYTOUCH_BASE_URL),
    "setup": "{base_url}/setup".format(base_url=COZYTOUCH_BASE_URL),
    "gateways": "{base_url}/setup/gateways".format(base_url=COZYTOUCH_BASE_URL),
    "devices": "{base_url}/setup/devices".format(base_url=COZYTOUCH_BASE_URL),
    "deviceInfo": "{base_url}/setup/devices/[device_url]/states".format(
        base_url=COZYTOUCH_BASE_URL
    ),
    "stateInfo": "{base_url}/setup/devices/[device_url]/states/[state_name]".format(
        base_url=COZYTOUCH_BASE_URL
    ),
    "apply": "{base_url}/exec/apply".format(base_url=COZYTOUCH_BASE_URL),
}

USER_AGENT = "Home assistant/Cozytouch"
API_THROTTLE = 60  # Delay minimum between API call


class DeviceType(TextEnum):
    """Device type."""

    POD = "Pod"
    HEATER = "AtlanticElectricalHeaterWithAdjustableTemperatureSetpoint"
    PILOT_WIRE_INTERFACE = "AtlanticElectricalHeater"
    WATER_HEATER = "DomesticHotWaterProduction"
    TEMPERATURE = "TemperatureSensor"
    CONTACT = "ContactSensor"
    OCCUPANCY = "OccupancySensor"
    ELECTRECITY = "CumulativeElectricPowerConsumptionSensor"

    @classmethod
    def sensors(cls):
        """Sensors method."""
        return [cls.TEMPERATURE, cls.CONTACT, cls.OCCUPANCY, cls.ELECTRECITY]


class DeviceState(TextEnum):
    """Device state."""

    ABSENCE_END_DATE_STATE = "core:AbsenceEndDateState"
    ABSENCE_START_DATE_STATE = "core:AbsenceStartDateState"
    AWAY_STATE = "core:HolidaysModeState"
    BOOST_ELECTRIC_POWER_CONSUMPTION_STATE = (
        "core:BoostElectricPowerConsumptionState"  # int
    )
    BOOST_END_DATE_STATE = "core:BoostEndDateState"  # dict
    BOOST_MODE_DURATION_STATE = "core:BoostModeDurationState"  # int
    BOOST_START_DATE_STATE = "core:BoostStartDateState"  # dict
    BOTTOM_TANK_WATER_TEMPERATURE_STATE = "core:BottomTankWaterTemperatureState"
    COMFORT_TARGET_TEMPERATURE_STATE = "core:ComfortTargetTemperatureState"
    COMFORT_TEMPERATURE_STATE = "core:ComfortRoomTemperatureState"
    CONNECTIVITY_STATE = "core:ConnectivityState"
    CONTACT_STATE = "core:ContactState"
    CONTROL_WATER_TARGET_TEMPERATURE_STATE = (
        "core:ControlWaterTargetTemperatureState"  # int
    )
    COUNTRY_CODE_STATE = "core:CountryCodeState"
    DATE_TIME_STATE = "core:DateTimeState"  # dict
    DHWP_SOFTWARE_VERSION_STATE = "core:DHWPSoftwareVersionState"  # string
    ECO_TARGET_TEMPERATURE_STATE = "core:EcoTargetTemperatureState"
    ECO_TEMPERATURE_STATE = "core:EcoRoomTemperatureState"
    ELECTRIC_ENERGY_CONSUMPTION_STATE = "core:ElectricEnergyConsumptionState"
    EXPECTED_NUM_SHOWER_STATE = "core:ExpectedNumberOfShowerState"  # int
    FROST_PROTECTION_TARGET_TEMPERATURE_STATE = (
        "core:FrostProtectionTargetTemperatureState"
    )
    HALTED_TARGET_TEMPERATURE_STATE = "core:HaltedTargetTemperatureState"
    HEATING_STATUS_STATE = "core:HeatingStatusState"  # bool off
    LAST_ACTION_CONF_BUTTON_STATE = "internal:LastActionConfigButtonState"
    LIGHTING_LED_POD_MODE_STATE = "internal:LightingLedPodModeState"
    MANUFACTURER_NAME_STATE = "core:ManufacturerNameState"  # string
    MAX_SHOWER_MANUEL_MODE_STATE = "core:MaximalShowerManualModeState"  # int
    MAX_TEMPERATURE_MANUEL_MODE_STATE = "core:MaximalTemperatureManualModeState"  # int
    MIDDLE_WATER_TEMPERATURE_IN_STATE = "core:MiddleWaterTemperatureInState"  # float
    MIN_SHOWER_MANUEL_MODE_STATE = "core:MinimalShowerManualModeState"  # int
    MIN_TEMPERATURE_MANUEL_MODE_STATE = "core:MinimalTemperatureManualModeState"  # int
    MODEL_STATE = "io:ModelState"
    NAME_STATE = "core:NameState"  # string
    NUM_SHOWER_REMAINING_STATE = "core:NumberOfShowerRemainingState"  # int
    NUM_TANK_STATE = "core:NumberOfTankState"  # int
    OCCUPANCY_STATE = "core:OccupancyState"
    ON_OFF_STATE = "core:OnOffState"
    OPERATING_MODE_STATE = "core:OperatingModeState"  # dict -> class OperatingModeState
    POWER_HEAT_ELECTRICAL_IN_STATE = "core:PowerHeatElectricalInState"  # int
    PRIORITY_LOCK_TIMER_STATE = "core:PriorityLockTimerState"
    PROGRAMMING_AVAILABLE_STATE = "core:ProgrammingAvailableState"  # int
    RSSI_LEVEL_STATE = "core:RSSILevelState"  # int 0-100
    SECURED_POSITION_TEMPERATURE_STATE = "core:SecuredPositionTemperatureState"
    STATUS_STATE = "core:StatusState"  # string available,unavailable
    STOP_RELAUNCH_STATE = "core:StopRelaunchState"
    TARGET_TEMPERATURE_STATE = "core:TargetTemperatureState"  # float
    TARGETING_HEATING_LEVEL_STATE = "io:TargetHeatingLevelState"
    TEMPERATURE_STATE = "core:TemperatureState"  # float
    V40_WATER_VOLUME_ESTIMATION_STATE = "core:V40WaterVolumeEstimationState"  # int
    VERSION_STATE = "core:VersionState"  # int
    WATER_CONSUMPTION_STATE = "core:WaterConsumptionState"  # int
    WATER_TARGET_TEMPERATURE_STATE = "core:WaterTargetTemperatureState"  # int
    WATER_TEMPERATURE_STATE = "core:WaterTemperatureState"  # int

    # Input/Output
    ANTI_LEGIONELLOSIS_STATE = "io:AntiLegionellosisState"  # bool 0/1
    AWAY_MODE_DURATION_STATE = "io:AwayModeDurationState"  # bool 0/1
    BOILER_INSTALLATION_OPTION_STATE = "io:BoilerInstallationOptionState"  # dict
    DHW_AWAY_STATE = "io:DHWAbsenceModeState"  # string off,on,prog
    DHW_BOOST_MODE_STATE = "io:DHWBoostModeState"  # string off,on,prog
    DHW_CAPACITY_STATE = "io:DHWCapacityState"  # float
    DHW_ERROR_STATE = "io:DHWErrorState"  # dict
    DHW_MODE_STATE = "io:DHWModeState"  # string
    ELECTRIC_BOOSTER_OPERATING_TIME_STATE = (
        "io:ElectricBoosterOperatingTimeState"  # int
    )
    ELECTRIC_EXTRA_MANAGEMENT_STATE = (
        "io:ElectricalExtraManagementState"  # string auto,deactive
    )
    EXTRACTION_OPTION_STATE = "io:ExtractionOptionState"  # string  fastExtractionSpeed,lowExtractionSpeed,noExtraction
    HEAT_PUMP_OPERATING_TIME_STATE = "io:HeatPumpOperatingTimeState"  # int
    INSTALLATION_STATE = "io:InstallationState"  # string -> class InstallationState
    MIDDLE_WATER_TEMPERATURE_STATE = "io:MiddleWaterTemperatureState"  # float
    OPERATING_MODE_CAPABILITIES_STATE = "io:OperatingModeCapabilitiesState"
    OPERATING_RANGE_STATE = "io:OperatingRangeState"  # string
    POWER_CONSUMPTION_FAN_STATE = "io:PowerConsumptionFanState"  # int
    POWER_HEAT_ELECTRICAL_STATE = "io:PowerHeatElectricalState"  # int
    POWER_HEAT_PUMP_STATE = "io:PowerHeatPumpState"  # int
    PRIORITY_LOCK_LEVEL_STATE = (
        "io:PriorityLockLevelState"  # string -> class PriorityLockLevelState
    )
    PRIORITY_LOCK_ORIGINATOR_STATE = (
        "io:PriorityLockOriginatorState"  # string -> class PriorityLockOriginatorState
    )
    PROGRAMMING_SLOTS_STATE = "io:ProgrammingSlotsState"  # dict
    RATE_MANAGEMENT_STATE = (
        "io:RateManagementState"  # string forbidden,no,recommended,unsuitable,wanted
    )
    SMART_GRID_OPTION_STATE = "io:SmartGridOptionState"  # string active,deactive


class OnOffState(TextEnum):
    """Set state."""

    ON = "on"
    OFF = "off"


class AwayModeState(TextEnum):
    """Set away mode."""

    ON = "on"
    OFF = "off"


class OperatingModeState(TextEnum):
    """Set operation mode."""

    STANDBY = "standby"
    BASIC = "basic"
    INTERNAL = "internal"
    AUTO = "auto"
    FROSTPROTECT = "frostprotection"
    MANUEL = "frostprotection"
    NORMAL = "normal"
    MAX = "max"
    PROG = "prog"
    PROGRAM = "program"


class OperatingRangeState(TextEnum):
    """Set operation range."""

    PAC24h = "pac24h_elec24h"
    PACPROG = "pacProg_elecProg"


class PriorityLockLevelState(TextEnum):
    """Priority Locke level."""

    COMFORTL1 = "comfortLevel1"
    COMFORTL2 = "comfortLevel2"
    COMFORTL3 = "comfortLevel3"
    COMFORTL4 = "comfortLevel4"
    ENVPROTECT = "environmentProtection"
    HUMPROTECT = "humanProtection"
    USERL1 = "userLevel1"
    USERL2 = "userLevel2"


class PriorityLockOriginatorState(TextEnum):
    """Priority Lock Originitor."""

    LSC = "LSC"
    SAAC = "SAAC"
    SFC = "SFC"
    UPS = "UPS"
    EXTERNALGATEWAY = "externalGateway"
    LOCALUSER = "localUser"
    MYSELF = "myself"
    RAIN = "rain"
    SECURITY = "security"
    TEMPERATURE = "temperature"
    TIMER = "timer"
    USER = "user"
    WIND = "wind"


class InstallationState(TextEnum):
    """Set installation state."""

    EXTRA_BOILER = "extraBoiler"
    EXTRA_SOLAR = "extraSolar"
    ONLY_THERMODYNAMIC = "onlyThermodynamic"


class TargetingHeatingLevelState(TextEnum):
    """Set targeting heating level state."""

    ECO = "eco"
    BOOST = "boost"
    COMFORT = "comfort"
    COMFORT_ONE = "comfort-1"
    COMFORT_TWO = "comfort-2"
    FROST_PROTECTION = "frostprotection"
    SECURED = "secured"
    OFF = "off"


class DeviceCommand(TextEnum):
    """Commande device."""

    DELAY_STOP_IDENTIFY = "delayedStopIdentify"
    GET_NAME = "getName"
    SET_ABSENCE_END_DATE = "setAbsenceEndDate"
    SET_ABSENCE_MODE = "setAbsenceMode"
    SET_ABSENCE_START_DATE = "setAbsenceStartDate"
    SET_AWAYS_MODE_DURATION = "setAwayModeDuration"
    SET_ANTI_LEGIONELLOSIS = "setAntiLegionellosis"
    SET_AWAY_MODE = "setHolidays"
    SET_BOILER_INSTALLATION_OPTION = "setBoilerInstallationOption"
    SET_BOOST_END_DATE = "setBoostEndDate"
    SET_BOOST_MODE = "setBoostMode"
    SET_BOOST_MODE_DURATION = "setBoostModeDuration"
    SET_BOOST_START_DATE = "setBoostStartDate"
    SET_COMFORT_TARGET_TEMP = "setComfortTargetTemperature"
    SET_COMFORT_TEMP = "setComfortTemperature"
    SET_CURRENT_OPERATION_MODE = "setCurrentOperatingMode"
    SET_DATETIME = "setDateTime"
    SET_DWH_MODE = "setDHWMode"
    SET_ECO_TARGET_TEMP = "setEcoTargetTemperature"
    SET_ECO_TEMP = "setEcoTemperature"
    SET_ELECTRICAL_EXTRA_MANAGEMENT = "setElectricalExtraManagement"
    SET_EXPECTED_NUM_SHOWER = "setExpectedNumberOfShower"
    SET_EXTRACTION_OPTION = "setExtractionOption"
    SET_FROST_PROTECT_TARGET_TEMP = "setFrostProtectionTargetTemperature"
    SET_HALTED_TARGET_TEMP = "setHaltedTargetTemperature"
    SET_HEATING_LEVEL = "setHeatingLevel"
    SET_INSTALLATION = "setInstallation"
    SET_LOWERING_TEMP_PROG = "setSetpointLoweringTemperatureInProgMode"
    SET_NAME = "setName"
    SET_OPERATING_RANGE = "setOperatingRange"
    SET_OPERATION_MODE = "setOperatingMode"
    SET_PROGRAMMING_SLOT = "setProgrammingSlots"
    SET_RATE_MANAGMENT = "setRateManagement"
    SET_SMART_GRID_OPTION = "setSmartGridOption"
    SET_TARGET_TEMP = "setTargetTemperature"
    SET_WATER_TARGET_TEMPERATURE = "setWaterTargetTemperature"
    SET_WATER_TEMPERATURE = "setWaterTemperature"

    REFRESH_ABSENCE_END_DATE = "refreshAbsenceEndDate"
    REFRESH_ABSENCE_MODE = "refreshAbsenceMode"
    REFRESH_ABSENCE_START_DATE = "refreshAbsenceStartDate"
    REFRESH_AWAYS_MODE_DURATION = "refreshAwayModeDuration"
    REFRESH_ANTI_LEGIONELLOSIS = "refreshAntiLegionellosis"
    REFRESH_BOILER_INSTALLATION_OPTION = "refreshBoilerInstallationOption"
    REFRESH_BOOST_END_DATE = "refreshBoostEndDate"
    REFRESH_BOOST_MODE = "refreshBoostMode"
    REFRESH_BOOST_MODE_DURATION = "refreshBoostModeDuration"
    REFRESH_BOOST_START_DATE = "refreshBoostStartDate"
    REFRESH_BOTTOM_TANK_WATER_TEMPERATURE = "refreshBottomTankWaterTemperature"
    REFRESH_COMFORT_TEMPERATURE = "refreshComfortTemperature"
    REFRESH_CURRENT_OPERATING_MODE = "refreshCurrentOperatingMode"
    REFRESH_DHW_CAPACITY = "refreshDHWCapacity"
    REFRESH_DHW_ERROR = "refreshDHWError"
    REFRESH_DHW_MODE = "refreshDHWMode"
    REFRESH_ECO_TEMPERATURE = "refreshEcoTemperature"
    REFRESH_ELECTRICAL_EXTRA_MANAGEMENT = "refreshElectricalExtraManagement"
    REFRESH_EXPECTED_NUM_SHOWER = "refreshExpectedNumberOfShower"
    REFRESH_EXTRACTION_OPTION = "refreshExtractionOption"
    REFRESH_HEATING_LEVEL = "refreshHeatingLevel"
    REFRESH_INSTALLATION = "refreshInstallation"
    REFRESH_LOWERING_TEMP_PROG = "refreshSetpointLoweringTemperatureInProgMode"
    REFRESH_MANUFACTURER_NAME = "refreshManufacturerName"
    REFRESH_MIDDLE_WATER_TEMPERATURE = "refreshMiddleWaterTemperature"
    REFRESH_MIDDLE_WATER_TEMPERATURE_IN = "refreshMiddleWaterTemperatureIn"
    REFRESH_OPERATING_MODE_CAPABILITIES = "refreshOperatingModeCapabilities"
    REFRESH_OPERATING_RANGE = "refreshOperatingRange"
    REFRESH_OPERATING_TIME = "refreshOperatingTime"
    REFRESH_OPERATION_MODE = "refreshOperatingMode"
    REFRESH_POD_MODE = "refreshPodMode"
    REFRESH_PROGRAMMING_SLOT = "refreshProgrammingSlots"
    REFRESH_RATE_MANAGMENT = "refreshRateManagement"
    REFRESH_SMART_GRID_OPTION = "refreshSmartGridOption"
    REFRESH_TARGET_TEMPERATURE = "refreshTargetTemperature"
    REFRESH_UPDATE_STATUS = "refreshUpdateStatus"
    REFRESH_WATER_CONSUMPTION = "refreshWaterConsumption"
    REFRESH_WATER_TARGET_TEMPERATURE = "refreshWaterTargetTemperature"
    REFRESH_WATER_TEMPERATURE = "refreshWaterTemperature"
