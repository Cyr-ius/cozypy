"""Describe objects for cozytouch."""
import logging
from cozytouchpy.constant import DeviceState as ds
from cozytouchpy.exception import CozytouchException
from cozytouchpy.utils import CozytouchAction, CozytouchCommand, CozytouchCommands, DeviceMetadata
from .gateway import CozytouchGateway
from .object import CozytouchObject
from .place import CozytouchPlace

logger = logging.getLogger(__name__)


class CozytouchDevice(CozytouchObject):
    """Device."""

    def __init__(self, data: dict):
        """Initialize."""
        super(CozytouchDevice, self).__init__(data)
        self.states = data.get("states", {})
        self.definition = data.get("definition", {})
        self.sensors = {}
        self.metadata: DeviceMetadata = None
        self.gateway: CozytouchGateway = None
        self.place: CozytouchPlace = None
        self.parent: CozytouchDevice = None

    @property
    def deviceUrl(self):
        """Device url."""
        return self.metadata.base_url

    @property
    def widget(self):
        """Widget."""
        return self.data.get("widget", "")

    @property
    def manufacturer(self):
        """Manufacturer."""
        return self.get_state(ds.MANUFACTURER_NAME_STATE)

    @property
    def model(self):
        """Model."""
        return self.get_state(ds.MODEL_STATE)

    @property
    def name(self):
        """Name."""
        return self.place.name + " " + self.widget.replace("_", " ").capitalize()

    @property
    def controllable_name(self):
        """Name."""
        return self.data["controllableName"]

    @property
    def version(self):
        """Version."""
        return self.get_state(ds.VERSION_STATE)

    def get_state(self, name, default=None):
        """Get state value."""
        for state in self.states:
            if state.get("name") == name:
                return state.get("value")
        return default

    def set_state(self, state, value):
        """Set state value."""
        for state_name in self.states:
            if state_name == state:
                state_name = value
                break

    def get_definition(self, definition, default=None):
        """Get definition value."""
        for state in self.data["definition"].get("states"):
            if state.get("qualifiedName") == definition:
                return state.get("values")
        return default

    def get_sensors(self, device_type, default=None):
        """Get sensor."""
        for sensor in self.sensors:
            if sensor.widget == device_type or sensor.controllable_name == device_type:
                return sensor
        return default

    async def set_mode(self, mode_state, actions):
        """Set mode."""
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        obj_commands = CozytouchCommands(f"Change {mode_state} mode")
        obj_action = CozytouchAction(device_url=self.deviceUrl)
        for action in actions:
            command, paramters = action
            self.has_state(mode_state, command, paramters)
            obj_action.add_command(CozytouchCommand(command, paramters))
        obj_commands.add_action(obj_action)
        await self.client.send_commands(obj_commands)

    def has_state(self, mode_state, command_name, parameters):
        """Search and check parameters."""
        state_type = [
            state["type"] for state in self.states if state["name"] == mode_state
        ]
        if len(state_type) == 0:
            raise CozytouchException("Unsupported state %s" % mode_state)

        state_command = [
            (command.get("commandName"), command.get("nparams"))
            for command in self.definition.get("commands")
            if command["commandName"] == command_name
        ]
        if len(state_command) != 1:
            raise CozytouchException("Unsupported command %s" % command_name)

        for state in self.definition.get("states"):
            if state["qualifiedName"] == mode_state and state_command[0][1] > 0:
                state_values = state.get("values")
                if 1 in state_type and not isinstance(parameters, int):
                    logger.warning("Unsupported Integer %s", parameters)
                if 2 in state_type and not isinstance(parameters, float):
                    logger.warning("Unsupported Float %s", parameters)
                if 3 in state_type and state_values:
                    if parameters not in state_values:
                        logger.warning(
                            "Unsupported '%s' value in %s", parameters, state_values
                        )
                if (10 in state_type or 11 in state_type) and not isinstance(parameters, list):
                    logger.warning("Unsupported List %s", parameters)

    async def update(self):
        """Update device."""
        if self.client is None:
            raise CozytouchException("Unable to execute command")
        logger.debug("Update states sensors")
        self.states = await self.client.get_device_state(self.deviceUrl)

    def __str__(self):
        """Definition."""
        return "{widget} (name={name}, model={model}, manufacturer={manufacturer}, version={version})".format(
            widget=self.widget.capitalize(),
            name=self.name,
            model=self.model,
            manufacturer=self.manufacturer,
            version=self.version,
        )
