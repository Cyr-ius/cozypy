"""Describe objects for cozytouch."""
import logging

from cozytouchpy.constant import DeviceState as ds
from cozytouchpy.utils import qualifiedname

from .device import CozytouchDevice

logger = logging.getLogger(__name__)


class CozytouchSensor(CozytouchDevice):
    """Generic sensor."""

    # @property
    # def id(self):
    #     """Return Unique id."""
    #     return self.parent.id + "_" + self.sensor_class

    @property
    def name(self):
        """Name."""
        return qualifiedname(self.data["controllableName"])

    @property
    def sensor_class(self):
        """Class."""
        return "unknown"


class CozytouchContactSensor(CozytouchSensor):
    """Contact sensor."""

    @property
    def sensor_class(self):
        """Class."""
        return "contact"

    @property
    def is_opened(self):
        """State."""
        state = self.get_state(ds.CONTACT_STATE)
        return state != "closed"


class CozytouchElectricitySensor(CozytouchSensor):
    """Electricity sensor."""

    @property
    def sensor_class(self):
        """Class."""
        return "consumption"

    @property
    def consumption(self):
        """State."""
        return int(self.get_state(ds.ELECTRIC_ENERGY_CONSUMPTION_STATE))


class CozytouchTemperatureSensor(CozytouchSensor):
    """Temperature sensor."""

    @property
    def sensor_class(self):
        """Class."""
        return "temperature"

    @property
    def temperature(self):
        """State."""
        return self.get_state(ds.TEMPERATURE_STATE)


class CozytouchOccupancySensor(CozytouchSensor):
    """Occupancy sensor."""

    @property
    def sensor_class(self):
        """Class."""
        return "occupancy"

    @property
    def is_occupied(self):
        """State."""
        return self.get_state(ds.OCCUPANCY_STATE) == "personInside"


class CozytouchCumulativeFossilEnergyConsumptionSensor(CozytouchSensor):
    """Temperature sensor."""

    @property
    def sensor_class(self):
        """Class."""
        return "consumption"

    @property
    def temperature(self):
        """State."""
        return self.get_state(ds.FOSSIL_ENERGY_CONSUMPTION_STATE)
