"""Describe objects for cozytouch."""
import logging

from .device import CozytouchDevice

logger = logging.getLogger(__name__)


class CozytouchPod(CozytouchDevice):
    """Pod."""

    @property
    def available(self):
        """Available status."""
        return self.data["available"]

    @property
    def is_on(self):
        """Is enable."""
        return self.data["enabled"]

    @property
    def supported_states(self) -> dict:
        """Supported states."""
        supported_states = [state["name"] for state in self.states]
        for sensor in self.sensors:
            sensor_states = [state["name"] for state in sensor.states]
            supported_states = list(set(supported_states + sensor_states))
        return supported_states

    def is_state_supported(self, state):
        """State."""
        return state in self.supported_states
