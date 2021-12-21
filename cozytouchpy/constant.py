"""Constants."""
from __future__ import annotations

from typing import Any

import attr


@attr.s(auto_attribs=True, slots=True, kw_only=True)
class OverkizServer:
    """Class to describe an Overkiz server."""

    name: str
    endpoint: str
    manufacturer: str
    configuration_url: str


class Command(dict):  # type: ignore
    """Represents an Command."""

    def __init__(self, name: str, parameters: list[str] | None = None, **_: Any):
        self.name = name
        self.parameters = parameters
        dict.__init__(self, name=name, parameters=parameters)


COZYTOUCH_ATLANTIC_API = "https://api.groupe-atlantic.com"
COZYTOUCH_CLIENT_ID = (
    "czduc0RZZXdWbjVGbVV4UmlYN1pVSUM3ZFI4YTphSDEzOXZmbzA1ZGdqeDJkSFVSQkFTbmhCRW9h"
)

SUPPORTED_SERVERS = {
    "atlantic_cozytouch": OverkizServer(
        name="Atlantic Cozytouch",
        endpoint="https://ha110-1.overkiz.com/enduser-mobile-web/enduserAPI/",
        manufacturer="Atlantic",
        configuration_url=None,
    )
}


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


class DeviceType:
    """Device type."""

    # Widget Actuator
    POD = "Pod"
    HEATER = "AtlanticElectricalHeaterWithAdjustableTemperatureSetpoint"
    PILOT_WIRE_INTERFACE = "AtlanticElectricalHeater"
    WATER_HEATER = "DomesticHotWaterProduction"
    APC_HEAT_PUMP = "AtlanticPassAPCHeatPump"
    APC_WATER_HEATER = "AtlanticPassAPCDHW"
    APC_HEATING_ZONE = "AtlanticPassAPCHeatingZone"
    APC_HEATING_COOLING_ZONE = "AtlanticPassAPCHeatingAndCoolingZone"
    APC_BOILER = "AtlanticPassAPCBoiler"

    # Widget Sensors
    TEMPERATURE = "TemperatureSensor"
    CONTACT = "ContactSensor"
    OCCUPANCY = "OccupancySensor"
    ELECTRICITY = "CumulativeElectricPowerConsumptionSensor"
    DHW_ELECTRICITY = "DHWRelatedElectricalEnergyConsumptionSensor"
    FOSSIL_ENERGY = "CumulativeFossilEnergyConsumptionSensor"

    # Actuators - Controllable Name
    PASS_APC_DHW = "io:AtlanticPassAPCDHWComponent"
    PASS_APC_BOILER_MAIN = "io:AtlanticPassAPCBoilerMainComponent"
    PASS_APC_HEATING_ZONE = "io:AtlanticPassAPCHeatingZoneComponent"
    PASS_APC_HEATINGANDCOOLING_ZONE = "io:AtlanticPassAPCHeatingAndCoolingZoneComponent"
    PASS_APC_HEATPUMP = "io:AtlanticPassAPCHeatPumpMainComponent"
    DHW_V2_FLATC2_IO = "io:AtlanticDomesticHotWaterProductionV2_CE_FLAT_C2_IOComponent"
    DHW_V2_THIV4_IO = "io:AtlanticDomesticHotWaterProductionV2_CETHI_V4_IOComponent"
    DHW_IO = "io:AtlanticDomesticHotWaterProductionIOComponent"
    DHW_V3_IO = "io:AtlanticDomesticHotWaterProductionV3IOComponent"
    DHW_V2_MURAL_IO = "io:AtlanticDomesticHotWaterProductionV2_MURAL_IOComponent"
    HEATER_IO = "io:AtlanticElectricalHeaterIOComponent"  # Pilot wire
    HEATER_SETPOINT_IO = (
        "io:AtlanticElectricalHeaterWithAdjustableTemperatureSetpointIOComponent"
    )

    # Sensors - Controllable Name
    PASS_APC_OUTSIDE_TEMP = "io:AtlanticPassAPCOutsideTemperatureSensor"
    PASS_APC_ZONE_TEMP = "io:AtlanticPassAPCZoneTemperatureSensor"
    CONTACT_IO_SYSTEM = "io:ContactIOSystemDeviceSensor"
    CUMULATED_ELECT_ENERGY_CONSUMP_IO_SYSTEM = (
        "io:CumulatedElectricalEnergyConsumptionIOSystemDeviceSensor"
    )
    DHW_CUMULATED_ELECT_ENERGY_CONSUMP_IO_SYSTEM = (
        "io:DHWCumulatedElectricalEnergyConsumptionIOSystemDeviceSensor"
    )
    OCCUPANCY_IO_SYSTEM = "io:OccupancyIOSystemDeviceSensor"
    TEMPERATURE_IN_CELCIUS_IO_SYSTEM = "io:TemperatureInCelciusIOSystemDeviceSensor"
    DHW_RELATED_ELECT_ENERGY_CONSUMP = "io:DHWRelatedElectricalEnergyConsumptionSensor"
    DHW_RELATED_FOSSIL_ENERGY_CONSUMP = "io:DHWRelatedFossilEnergyConsumptionSensor"
    HEATING_RELATED_ELECT_ENERGY_CONSUMP = (
        "io:HeatingRelatedElectricalEnergyConsumptionSensor"
    )
    COOLING_RELATED_ELECT_ENERGY_CONSUMP = (
        "io:CoolingRelatedElectricalEnergyConsumptionSensor"
    )
    TOTAL_ELECT_ENERGY_CONSUMP = "io:TotalElectricalEnergyConsumptionSensor"
    TOTAL_FOSSIL_ENERGY_CONSUMP = "io:TotalFossilEnergyConsumptionSensor"

    # Class Sensors
    CLASS_TEMPERATURE = [TEMPERATURE]
    CLASS_CONTACT = [CONTACT]
    CLASS_OCCUPANCY = [OCCUPANCY]
    CLASS_ELECTRICITY = [ELECTRICITY, DHW_ELECTRICITY]
    CLASS_FOSSIL = [FOSSIL_ENERGY]

    # Class Actuators
    CLASS_BOILER = [APC_BOILER]
    CLASS_CLIMATE = [APC_HEATING_ZONE, APC_HEATING_COOLING_ZONE]
    CLASS_HEATER = [HEATER, PILOT_WIRE_INTERFACE]
    CLASS_HEATPUMP = [APC_HEAT_PUMP]
    CLASS_POD = [POD]
    CLASS_WATERHEATER = [WATER_HEATER, APC_WATER_HEATER]

    @classmethod
    def sensors(cls):
        """Sensors method."""
        return [
            cls.TEMPERATURE,
            cls.CONTACT,
            cls.OCCUPANCY,
            cls.ELECTRICITY,
            cls.DHW_ELECTRICITY,
            cls.FOSSIL_ENERGY,
        ]

    @classmethod
    def actuators(cls):
        """Sensors method."""
        return [
            cls.CLASS_BOILER,
            cls.CLASS_CLIMATE,
            cls.CLASS_HEATER,
            cls.CLASS_HEATPUMP,
            cls.CLASS_POD,
            cls.CLASS_WATERHEATER,
        ]


class DeviceState:
    """Device state."""

    ABSENCE_COOLING_TARGET_TEMPERATURE_STATE = (
        "core:AbsenceCoolingTargetTemperatureState"
    )
    ABSENCE_END_DATE_STATE = "core:AbsenceEndDateState"
    ABSENCE_HEATING_TARGET_TEMPERATURE_STATE = (
        "core:AbsenceHeatingTargetTemperatureState"
    )
    ABSENCE_START_DATE_STATE = "core:AbsenceStartDateState"
    ACTIVE_COOLING_TIME_PROGRAM_STATE = "core:ActiveCoolingTimeProgramState"
    ACTIVE_HEATING_TIME_PROGRAM_STATE = "core:ActiveHeatingTimeProgramState"
    AWAY_STATE = "core:HolidaysModeState"
    BOOST_ELECTRIC_POWER_CONSUMPTION_STATE = "core:BoostElectricPowerConsumptionState"
    BOOST_END_DATE_STATE = "core:BoostEndDateState"
    BOOST_MODE_DURATION_STATE = "core:BoostModeDurationState"
    BOOST_ON_OFF_STATE = "core:BoostOnOffState"
    BOOST_START_DATE_STATE = "core:BoostStartDateState"
    BOTTOM_TANK_WATER_TEMPERATURE_STATE = "core:BottomTankWaterTemperatureState"
    COMFORT_COOLING_TARGET_TEMPERATURE_STATE = (
        "core:ComfortCoolingTargetTemperatureState"
    )
    COMFORT_HEATING_TARGET_TEMPERATURE_STATE = (
        "core:ComfortHeatingTargetTemperatureState"
    )
    COMFORT_TARGET_TEMPERATURE_STATE = "core:ComfortTargetTemperatureState"
    COMFORT_TARGET_DHW_TEMPERATURE_STATE = "core:ComfortTargetDHWTemperatureState"
    COMFORT_TEMPERATURE_STATE = "core:ComfortRoomTemperatureState"
    CONNECTIVITY_STATE = "core:ConnectivityState"
    CONTACT_STATE = "core:ContactState"
    CONTROL_WATER_TARGET_TEMPERATURE_STATE = "core:ControlWaterTargetTemperatureState"
    COOLING_ON_OFF_STATE = "core:CoolingOnOffState"
    COUNTRY_CODE_STATE = "core:CountryCodeState"
    DATE_TIME_STATE = "core:DateTimeState"
    DEROGATED_TARGET_TEMPERATURE_STATE = "core:DerogatedTargetTemperatureState"
    DEROGATION_ON_OFF_STATE = "core:DerogationOnOffState"
    DHW_DEROGATION_AVAILABILITY_STATE = "core:DHWDerogationAvailabilityState"
    DHW_ON_OFF_STATE = "core:DHWOnOffState"
    DHWP_SOFTWARE_VERSION_STATE = "core:DHWPSoftwareVersionState"
    ECO_COOLING_TARGET_TEMPERATURE_STATE = "core:EcoCoolingTargetTemperatureState"
    ECO_HEATING_TARGET_TEMPERATURE_STATE = "core:EcoHeatingTargetTemperatureState"
    ECO_TARGET_TEMPERATURE_STATE = "core:EcoTargetTemperatureState"
    ECO_TARGET_DHW_TEMPERATURE_STATE = "core:EcoTargetDHWTemperatureState"
    ECO_TEMPERATURE_STATE = "core:EcoRoomTemperatureState"
    ECS_POWER_CONSUMPTION_EXTRA1_STATE = "core:ECSPowerConsumptionExtra1State"
    ECS_POWER_CONSUMPTION_EXTRA2_STATE = "core:ECSPowerConsumptionExtra2State"
    ECS_POWER_CONSUMPTION_EXTRA3_STATE = "core:ECSPowerConsumptionExtra3State"
    ECS_POWER_CONSUMPTION_STATE = "core:ECSPowerConsumptionState"
    ELECTRIC_ENERGY_CONSUMPTION_STATE = "core:ElectricEnergyConsumptionState"
    ERROR_CODE_STATE = "core:ErrorCodeState"
    EXPECTED_NUM_SHOWER_STATE = "core:ExpectedNumberOfShowerState"
    FROST_PROTECTION_TARGET_TEMPERATURE_STATE = (
        "core:FrostProtectionTargetTemperatureState"
    )
    FOSSIL_ENERGY_CONSUMPTION_STATE = "core:FossilEnergyConsumptionState"
    HALTED_TARGET_TEMPERATURE_STATE = "core:HaltedTargetTemperatureState"
    HEATING_DEROGATION_AVAILABILITY_STATE = "core:HeatingDerogationAvailabilityState"
    HEATING_ON_OFF_STATE = "core:HeatingOnOffState"
    HEATING_POWER_CONSUMPTION_EXTRA1_STATE = "core:HeatingPowerConsumptionExtra1State"
    HEATING_POWER_CONSUMPTION_EXTRA2_STATE = "core:HeatingPowerConsumptionExtra2State"
    HEATING_POWER_CONSUMPTION_EXTRA3_STATE = "core:HeatingPowerConsumptionExtra3State"
    HEATING_POWER_CONSUMPTION_STATE = "core:HeatingPowerConsumptionState"
    HEATING_STATUS_STATE = "core:HeatingStatusState"
    LAST_ACTION_CONF_BUTTON_STATE = "internal:LastActionConfigButtonState"
    LIGHTING_LED_POD_MODE_STATE = "internal:LightingLedPodModeState"
    MANUFACTURER_NAME_STATE = "core:ManufacturerNameState"
    MAX_SHOWER_MANUEL_MODE_STATE = "core:MaximalShowerManualModeState"
    MAX_TEMPERATURE_MANUEL_MODE_STATE = "core:MaximalTemperatureManualModeState"
    MIDDLE_WATER_TEMPERATURE_IN_STATE = "core:MiddleWaterTemperatureInState"
    MIN_SHOWER_MANUEL_MODE_STATE = "core:MinimalShowerManualModeState"
    MIN_TEMPERATURE_MANUEL_MODE_STATE = "core:MinimalTemperatureManualModeState"
    NAME_STATE = "core:NameState"
    NUM_SHOWER_REMAINING_STATE = "core:NumberOfShowerRemainingState"
    NUM_TANK_STATE = "core:NumberOfTankState"
    OCCUPANCY_STATE = "core:OccupancyState"
    ON_OFF_STATE = "core:OnOffState"
    OPERATING_MODE_STATE = "core:OperatingModeState"
    POWER_HEAT_ELECTRICAL_IN_STATE = "core:PowerHeatElectricalInState"
    PRIORITY_LOCK_TIMER_STATE = "core:PriorityLockTimerState"
    PRODUCT_MODEL_NAME_STATE = "core:ProductModelNameState"
    PROGRAMMING_AVAILABLE_STATE = "core:ProgrammingAvailableState"
    RSSI_LEVEL_STATE = "core:RSSILevelState"
    SECURED_POSITION_TEMPERATURE_STATE = "core:SecuredPositionTemperatureState"
    STATUS_STATE = "core:StatusState"
    STOP_RELAUNCH_STATE = "core:StopRelaunchState"
    TARGET_DHW_TEMPERATURE_STATE = "core:TargetDHWTemperatureState"
    TARGET_TEMPERATURE_STATE = "core:TargetTemperatureState"
    TEMPERATURE_STATE = "core:TemperatureState"
    THERMAL_CONFIGURATION_STATE = "core:ThermalConfigurationState"
    TIME_PROGRAM1_STATE = "core:TimeProgram1State"
    TIME_PROGRAM2_STATE = "core:TimeProgram2State"
    TIME_PROGRAM3_STATE = "core:TimeProgram3State"
    TIME_PROGRAM4_STATE = "core:TimeProgram4State"
    V40_WATER_VOLUME_ESTIMATION_STATE = "core:V40WaterVolumeEstimationState"
    VERSION_STATE = "core:VersionState"
    WATER_CONSUMPTION_STATE = "core:WaterConsumptionState"
    WATER_TARGET_TEMPERATURE_STATE = "core:WaterTargetTemperatureState"
    WATER_TEMPERATURE_STATE = "core:WaterTemperatureState"
    ZONES_NUMBER_STATE = "core:ZonesNumberState"

    # Input/Output
    ABSENCE_SCHEDULING_AVAILABILITY_STATE = "io:AbsenceSchedulingAvailabilityState"
    ABSENCE_SCHEDULING_MODE_STATE = "io:AbsenceSchedulingModeState"
    ANTI_LEGIONELLOSIS_STATE = "io:AntiLegionellosisState"
    AWAY_MODE_DURATION_STATE = "io:AwayModeDurationState"
    BOILER_INSTALLATION_OPTION_STATE = "io:BoilerInstallationOptionState"
    COOLING_INTERNAL_SCHEDULING_AVAILABILITY_STATE = (
        "io:CoolingInternalSchedulingAvailabilityState"
    )
    DEROGATION_REMAINING_TIME_STATE = "io:DerogationRemainingTimeState"
    DHW_ABSENCE_MODE_STATE = "io:DHWAbsenceModeState"  # V2_CE_FLAT_C2_IOComponent
    DHW_AVAILABILITY_STATE = "io:DHWAvailabilityState"
    DHW_AWAY_STATE = "io:DHWAbsenceModeState"
    DHW_BOOST_MODE_STATE = "io:DHWBoostModeState"
    DHW_CAPACITY_STATE = "io:DHWCapacityState"
    DHW_ERROR_STATE = "io:DHWErrorState"
    DHW_MODE_STATE = "io:DHWModeState"
    ELECTRIC_BOOSTER_OPERATING_TIME_STATE = "io:ElectricBoosterOperatingTimeState"
    ELECTRIC_EXTRA_MANAGEMENT_STATE = "io:ElectricalExtraManagementState"
    ENERGY_CONSUMPTION_AVAILABILITY_STATE = "io:EnergyConsumptionAvailabilityState"
    EXTRACTION_OPTION_STATE = "io:ExtractionOptionState"
    HEATING_INTERNAL_SCHEDULING_AVAILABILITY_STATE = (
        "io:HeatingInternalSchedulingAvailabilityState"
    )
    HEAT_PUMP_OPERATING_TIME_STATE = "io:HeatPumpOperatingTimeState"
    INSTALLATION_STATE = "io:InstallationState"
    LAST_PASS_APC_OPERATING_MODE_STATE = "io:LastPassAPCOperatingModeState"
    MIDDLE_WATER_TEMPERATURE_STATE = "io:MiddleWaterTemperatureState"
    MODEL_STATE = "io:ModelState"
    OPERATING_MODE_CAPABILITIES_STATE = "io:OperatingModeCapabilitiesState"
    OPERATING_RANGE_STATE = "io:OperatingRangeState"
    PASS_APC_COOLING_MODE_STATE = "io:PassAPCCoolingModeState"
    PASS_APC_COOLING_PROFILE_STATE = "io:PassAPCCoolingProfileState"
    PASS_APC_DHW_CONFIGURATION_STATE = "io:PassAPCDHWConfigurationState"
    PASS_APC_DHW_MODE_STATE = "io:PassAPCDHWModeState"
    PASS_APC_DHW_PROFILE_STATE = "io:PassAPCDHWProfileState"
    PASS_APC_HEATING_MODE_STATE = "io:PassAPCHeatingModeState"
    PASS_APC_HEATING_PROFILE_STATE = "io:PassAPCHeatingProfileState"
    PASS_APC_OPERATING_MODE_STATE = "io:PassAPCOperatingModeState"
    PASS_APC_PRODUCT_TYPE_STATE = "io:PassAPCProductTypeState"
    POWER_CONSUMPTION_FAN_STATE = "io:PowerConsumptionFanState"
    POWER_HEAT_ELECTRICAL_STATE = "io:PowerHeatElectricalState"
    POWER_HEAT_PUMP_STATE = "io:PowerHeatPumpState"
    PRIORITY_LOCK_LEVEL_STATE = "io:PriorityLockLevelState"
    PRIORITY_LOCK_ORIGINATOR_STATE = "io:PriorityLockOriginatorState"
    PROGRAMMING_SLOTS_STATE = "io:ProgrammingSlotsState"
    RATE_MANAGEMENT_STATE = "io:RateManagementState"
    SMART_GRID_OPTION_STATE = "io:SmartGridOptionState"
    TARGETING_HEATING_LEVEL_STATE = "io:TargetHeatingLevelState"
    THERMAL_SCHEDULING_AVAILABILITY_STATE = "io:ThermalSchedulingAvailabilityState"
    THERMAL_SCHEDULING_MODE_STATE = "io:ThermalSchedulingModeState"


class OnOffState:
    """Set state."""

    ON = "on"
    OFF = "off"


class AvailableState:
    """Set away mode."""

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


class ThermalState:
    """Set thermal mode."""

    COOL = "cooling"
    HEAT = "heating"
    HEATCOOL = "heatingAndCooling"


class ModeState:
    """Set operation mode."""

    AWAY = "away"
    ABSENCE = "absence"
    AUTO = "auto"
    BASIC = "basic"
    BOOST = "boost"
    COMFORT = "comfort"
    COMFORT_ONE = "comfort-1"
    COMFORT_TWO = "comfort-2"
    COOLING = "cooling"
    DRYING = "drying"
    ECO = "eco"
    EXTERNAL_SCHEDULING = "externalScheduling"
    FROSTPROTECT = "frostprotection"
    HEATING = "heating"
    INTERNAL = "internal"
    INTERNAL_SCHEDULING = "internalScheduling"
    MANU = "manu"
    MANUEL = "manuel"
    MAX = "max"
    NORMAL = "normal"
    OFF = "off"
    PROG = "prog"
    PROGRAM = "program"
    SECURED = "secured"
    STANDBY = "standby"
    STOP = "stop"


class DeviceCommand:
    """Commande device."""

    SET_ABSENCE_HEATING_TARGET_TEMP = "setAbsenceHeatingTargetTemperature"
    SET_ABSENCE_COOLING_TARGET_TEMP = "setAbsenceCoolingTargetTemperature"
    SET_ABSENCE_END_DATE_TIME = "setAbsenceEndDateTime"
    SET_ABSENCE_START_DATE_TIME = "setAbsenceStartDateTime"
    SET_ABSENCE_MODE = "setAbsenceMode"  # V2_CE_FLAT_C2_IOComponent
    SET_AWAY_MODE = "setHolidays"
    SET_AWAYS_MODE_DURATION = "setAwayModeDuration"
    SET_BOOST_MODE = "setBoostMode"
    SET_BOOST_MODE_DURATION = "setBoostModeDuration"
    SET_COMFORT_COOLING_TARGET_TEMPERATURE = "setComfortCoolingTargetTemperature"
    SET_COMFORT_HEATING_TARGET_TEMPERATURE = "setComfortHeatingTargetTemperature"
    SET_COMFORT_TARGET_DHW_TEMPERATURE = "setComfortTargetDHWTemperature"
    SET_COMFORT_TEMP = "setComfortTemperature"
    SET_COOLING_ON_OFF_STATE = "setCoolingOnOffState"
    SET_CURRENT_OPERATING_MODE = "setCurrentOperatingMode"
    SET_DEROGATION_ON_OFF_STATE = "setDerogationOnOffState"
    SET_DEROGATED_TARGET_TEMP = "setDerogatedTargetTemperature"
    SET_DWH_MODE = "setDHWMode"
    SET_ECO_COOLING_TARGET_TEMPERATURE = "setEcoCoolingTargetTemperature"
    SET_ECO_HEATING_TARGET_TEMPERATURE = "setEcoHeatingTargetTemperature"
    SET_ECO_TARGET_DHW_TEMPERATURE = "setEcoTargetDHWTemperature"
    SET_ECO_TEMP = "setEcoTemperature"
    SET_HEATING_LEVEL = "setHeatingLevel"
    SET_HEATING_ON_OFF_STATE = "setHeatingOnOffState"
    SET_OPERATING_MODE = "setOperatingMode"
    SET_PASS_APC_COOLING_MODE = "setPassAPCCoolingMode"
    SET_PASS_APC_DHW_MODE = "setPassAPCDHWMode"
    SET_PASS_APC_HEATING_MODE = "setPassAPCHeatingMode"
    SET_PASS_APC_OPERATING_MODE = "setPassAPCOperatingMode"
    SET_TARGET_TEMP = "setTargetTemperature"

    REFRESH_ABSENCE_MODE = "refreshAbsenceMode"  # V2_CE_FLAT_C2_IOComponent
    REFRESH_ABSENCE_SCHEDULING_AVAILABLE = "refreshAbsenceSchedulingAvailability"
    REFRESH_AWAYS_MODE_DURATION = "refreshAwayModeDuration"
    REFRESH_BOOST_MODE = "refreshBoostMode"
    REFRESH_BOOST_MODE_DURATION = "refreshBoostModeDuration"
    REFRESH_COMFORT_COOLING_TARGET_TEMPERATURE = (
        "refreshComfortCoolingTargetTemperature"
    )
    REFRESH_COMFORT_HEATING_TARGET_TEMPERATURE = (
        "refreshComfortHeatingTargetTemperature"
    )
    REFRESH_COMFORT_TARGET_DHW_TEMPERATURE = "refreshComfortTargetDHWTemperature"
    REFRESH_COMFORT_TEMPERATURE = "refreshComfortTemperature"
    REFRESH_DHW_MODE = "refreshDHWMode"
    REFRESH_ECO_COOLING_TARGET_TEMPERATURE = "refreshEcoCoolingTargetTemperature"
    REFRESH_ECO_HEATING_TARGET_TEMPERATURE = "refreshEcoHeatingTargetTemperature"
    REFRESH_ECO_TARGET_DHW_TEMPERATURE = "refreshEcoTargetDHWTemperature"
    REFRESH_ECO_TEMPERATURE = "refreshEcoTemperature"
    REFRESH_LOWERING_TEMP_PROG = "refreshSetpointLoweringTemperatureInProgMode"
    REFRESH_OPERATING_MODE = "refreshOperatingMode"
    REFRESH_OPERATION_MODE = "refreshOperationMode"
    REFRESH_PASS_APC_COOLING_MODE = "refreshPassAPCCoolingMode"
    REFRESH_PASS_APC_DHW_MODE = "refreshPassAPCDHWMode"
    REFRESH_PASS_APC_HEATING_MODE = "refreshPassAPCHeatingMode"
    REFRESH_TARGET_TEMPERATURE = "refreshTargetTemperature"
