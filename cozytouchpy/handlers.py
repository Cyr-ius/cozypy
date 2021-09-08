"""Construct class cozytouch."""

import logging
from .constant import DeviceType as dt
from .exception import CozytouchException
from .utils import DeviceMetadata
from .objects import (
    CozytouchClimate,
    CozytouchDevice,
    CozytouchPlace,
    CozytouchGateway,
    CozytouchHeater,
    CozytouchHeatPump,
    CozytouchPod,
    CozytouchWaterHeater,
    CozytouchBoiler,
    CozytouchContactSensor,
    CozytouchCumulativeFossilEnergyConsumptionSensor,
    CozytouchElectricitySensor,
    CozytouchOccupancySensor,
    CozytouchTemperatureSensor,
)

logger = logging.getLogger(__name__)


class Handler:
    """Set handler."""

    def __init__(self, data, client):
        """Initialize handler."""
        self.client = client
        self.data = data
        self.places = {}
        self.sensors = {}
        self.devices = {}
        self.__build_places(data["rootPlace"])
        self.__build_gateways(data["gateways"])
        self.__build_devices(data["devices"])

    def __build_places(self, place):
        self.places.update({place["oid"]: CozytouchPlace(place)})
        for subplace in place["subPlaces"]:
            self.__build_places(subplace)

    def __build_gateways(self, gateways):
        self.gateways = {}
        for gateway in gateways:
            place = self.__find_place(gateway)
            self.gateways.update({gateway["gatewayId"]: CozytouchGateway(gateway, place)})

    def __build_devices(self, devices):
        sensors = {}
        actuators = {}
        for device in devices:
            if device["definition"]["type"] == "SENSOR":
                sensors.update({device["oid"]: device})
            elif device["definition"]["type"] == "ACTUATOR":
                actuators.update({device["oid"]: device})
        for key, device in actuators.items():
            try:
                metadata = self.parse_url(device["deviceURL"])
                gateway = self.__find_gateway(metadata.gateway_id)
                place = self.__find_place(device)
                cozyouch_device = self.__build(
                    data=device,
                    client=self.client,
                    metadata=metadata,
                    gateway=gateway,
                    place=place,
                )
                self.devices.update({key: cozyouch_device})
                device_sensors = self.__link_sensors(
                    sensors, place, gateway, cozyouch_device
                )
                cozyouch_device.sensors = device_sensors

            except CozytouchException as error:
                logger.warning("Error building device, skipping: %s", error)

    @staticmethod
    def parse_url(url):
        """Parse url."""
        scheme = url[0 : url.find("://")]
        if scheme not in ["io", "internal", "modbuslink"]:
            raise CozytouchException("Invalid url {url}".format(url=url))
        metadata = DeviceMetadata()
        metadata.scheme = scheme
        parts = url.replace(scheme + "://", "").replace("#", "/").split("/")
        parts_len = len(parts)
        if parts_len < 2:
            raise CozytouchException("Invalid url {url}".format(url=url))
        metadata.gateway_id = parts[0]
        metadata.device_id = parts[1]
        if parts_len == 3:
            metadata.entity_id = parts[2]
        return metadata

    def __link_sensors(
        self,
        sensors,
        place: CozytouchPlace,
        gateway: CozytouchGateway,
        parent: CozytouchDevice,
    ):
        device_sensors = {}
        for sensor in sensors.values():
            metadata = self.parse_url(sensor["deviceURL"])
            if metadata.device_id == parent.metadata.device_id:
                sensor = {
                    sensor["oid"]: self.__build(
                        data=sensor,
                        client=self.client,
                        metadata=metadata,
                        gateway=gateway,
                        place=place,
                        parent=parent,
                    )
                }
                device_sensors.update(sensor)
        self.sensors.update(device_sensors)
        return device_sensors

    def __find_place(self, device):
        for place in self.places.values():
            if place.id == device["placeOID"]:
                return place
        raise CozytouchException(
            "Place {name} not found".format(name=device["placeOID"])
        )

    def __find_gateway(self, gateway_id):
        for gateway in self.gateways.values():
            if gateway.id == gateway_id:
                return gateway
        raise CozytouchException("Gateway {id} not found".format(id=gateway_id))

    def __build(self, data, client=None, metadata=None, gateway=None, place=None, sensors=None, parent=None):
        """Build device object."""
        if sensors is None:
            sensors = {}
        device = None
        if "widget" not in data or "uiClass" not in data:
            raise CozytouchException("Unable to identify device")
        device_class = data["widget"] if "widget" in data else data["uiClass"]
        if device_class in dt.CLASS_OCCUPANCY:
            device = CozytouchOccupancySensor(data)
            device.category = "sensor"
        elif device_class in dt.CLASS_TEMPERATURE:
            device = CozytouchTemperatureSensor(data)
            device.category = "sensor"
        elif device_class in dt.CLASS_ELECTRICITY:
            device = CozytouchElectricitySensor(data)
            device.category = "sensor"
        elif device_class in dt.CLASS_CONTACT:
            device = CozytouchContactSensor(data)
            device.category = "sensor"
        elif device_class in dt.CLASS_FOSSIL:
            device = CozytouchCumulativeFossilEnergyConsumptionSensor(data)
            device.category = "sensor"
        elif device_class in dt.CLASS_BOILER:
            device = CozytouchBoiler(data)
            device.category = "boiler"
        elif device_class in dt.CLASS_CLIMATE:
            device = CozytouchClimate(data)
            device.category = "climate"
        elif device_class in dt.CLASS_HEATER:
            device = CozytouchHeater(data)
            device.category = "heater"
        elif device_class in dt.CLASS_HEATPUMP:
            device = CozytouchHeatPump(data)
            device.category = "heatpump"
        elif device_class in dt.CLASS_POD:
            device = CozytouchPod(data)
            device.category = "pod"
        elif device_class in dt.CLASS_WATERHEATER:
            device = CozytouchWaterHeater(data)
            device.category = "waterheater"
        if device is None:
            raise CozytouchException("Unknown device {type}".format(type=device_class))

        device.client = client
        device.metadata = metadata
        device.gateway = gateway
        device.place = place
        device.parent = parent
        return device
