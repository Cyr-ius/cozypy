"""Cozytouch API."""
from __future__ import annotations

import backoff
import logging
from json import JSONDecodeError
from typing import Any, Dict, List, Union

from aiohttp import (ClientResponse, ClientSession, FormData,
                     ServerDisconnectedError)

from .constant import COZYTOUCH_ATLANTIC_API, COZYTOUCH_CLIENT_ID, Command
from .exception import AuthentificationFailed, CozytouchException
from .handlers import Handler

JSON = Union[Dict[str, Any], List[Dict[str, Any]]]

logger = logging.getLogger(__name__)


async def relogin(invocation: dict[str, Any]) -> None:
    await invocation["args"][0].connect()


async def refresh_listener(invocation: dict[str, Any]) -> None:
    await invocation["args"][0].register_event_listener()


class CozytouchClient:
    """Client session."""

    def __init__(self, username, password, server, session=None):
        """Initialize session."""
        self.username = username
        self.password = password
        self.server = server
        self.session = session if session else ClientSession()
        self.event_listener_id = None
        self._devices_info = {}

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type=None, exc_value=None, traceback=None):
        await self.close()

    async def close(self) -> None:
        """Close the session."""
        if self.event_listener_id:
            await self.unregister_event_listener()
        await self.session.close()

    async def __post(
        self, path: str, payload: JSON | None = None, data: JSON | None = None
    ) -> Any:
        """Make a POST request to API"""
        async with self.session.post(
            f"{self.server.endpoint}{path}",
            data=data,
            json=payload,
        ) as response:
            await self.check_response(response)
            return await response.json()

    async def __get(self, path: str) -> Any:
        """Make a GET request to the API"""
        async with self.session.get(f"{self.server.endpoint}{path}") as response:
            await self.check_response(response)
            return await response.json()

    async def connect(
        self,
        register_event_listener: bool | None = True,
    ) -> bool:

        jwt = await self.get_token()
        payload = {"jwt": jwt}

        response = await self.__post("login", data=payload)
        if response.get("success"):
            if register_event_listener:
                await self.register_event_listener()
            return True

        return False

    async def get_token(self):
        """Authenticate via CozyTouch identity and acquire JWT token."""
        # Request access token
        async with self.session.post(
            COZYTOUCH_ATLANTIC_API + "/token",
            data=FormData(
                {
                    "grant_type": "password",
                    "username": self.username,
                    "password": self.password,
                }
            ),
            headers={
                "Authorization": f"Basic {COZYTOUCH_CLIENT_ID}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        ) as response:
            token = await response.json()

            # {'error': 'invalid_grant',
            # 'error_description': 'Provided Authorization Grant is invalid.'}
            if "error" in token and token["error"] == "invalid_grant":
                raise CozytouchException(token["error_description"])

            if "token_type" not in token:
                raise CozytouchException("No CozyTouch token provided.")

        # Request JWT
        async with self.session.get(
            COZYTOUCH_ATLANTIC_API + "/gacoma/gacomawcfservice/accounts/jwt",
            headers={"Authorization": f"Bearer {token['access_token']}"},
        ) as response:
            jwt = await response.text()

            if not jwt:
                raise CozytouchException("No JWT token provided.")

            jwt = jwt.strip('"')  # Remove surrounding quotes

            return jwt

    @backoff.on_exception(
        backoff.expo,
        (CozytouchException, ServerDisconnectedError),
        max_tries=2,
        on_backoff=relogin,
    )
    async def get_setup(self):
        """Get cozytouch setup (devices, places)."""
        response = await self.__get("setup")
        return Handler(response, self)

    @backoff.on_exception(
        backoff.expo,
        (CozytouchException, ServerDisconnectedError),
        max_tries=2,
        on_backoff=relogin,
    )
    async def get_devices_data(self):
        """Fetch data."""
        response = await self.__get("setup/devices")
        return response

    async def get_devices(self):
        """Get all devices (devices, places)."""
        setup = await self.get_setup()
        return setup.devices

    async def get_devices_info(self):
        """Get all infos device."""
        data = await self.get_devices_data()
        for dev in data:
            metadata = Handler.parse_url(dev["deviceURL"])
            self._devices_info[metadata.base_url] = dev
        return self._devices_info

    async def get_device_state(self, device_url):
        """Get device info (devices, places)."""
        datas = await self.get_devices_info()

        if device_url not in datas:
            raise CozytouchException(
                "Unable to retrieve device {device_url}: not in available devices".format(
                    device_url=device_url
                )
            )
        return datas.get(device_url).get("states")

    async def get_device(self, device_url):
        """Get device object (devices, places)."""
        devices = await self.get_devices()

        for item in devices.values():
            if item.deviceUrl == device_url:
                return item
        return None

    @backoff.on_exception(
        backoff.expo,
        (AuthentificationFailed, ServerDisconnectedError),
        max_tries=2,
        on_backoff=relogin,
    )
    async def get_places(self):
        """List the places"""
        response = await self.__get("setup/places")
        return response

    @backoff.on_exception(
        backoff.expo, AuthentificationFailed, max_tries=2, on_backoff=relogin
    )
    async def send_commands(
        self,
        device_url: str,
        commands: list[Command],
        label: str | None = "python-api",
    ) -> str:
        """Send several commands in one call"""
        if isinstance(commands, str):
            commands = Command(commands)

        payload = {
            "label": label,
            "actions": [{"deviceURL": device_url, "commands": [commands]}],
        }
        response = await self.__post("exec/apply", payload)
        return response["execId"]

    @staticmethod
    async def check_response(response: ClientResponse) -> None:
        """Check the response returned by API"""
        if response.status in [200, 204]:
            return

        try:
            result = await response.json(content_type=None)
        except JSONDecodeError as error:
            result = await response.text()
            if "Server is down for maintenance" in result:
                raise CozytouchException("Server is down for maintenance") from error
            raise Exception(
                f"Unknown error while requesting {response.url}. {response.status} - {result}"
            ) from error

        if result.get("errorCode"):
            message = result.get("error")

            # {"errorCode": "AUTHENTICATION_ERROR",
            # "error": "Too many requests, try again later : login with xxx@xxx.tld"}
            if "Too many requests" in message:
                raise AuthentificationFailed(message)

            # {"errorCode": "AUTHENTICATION_ERROR", "error": "Bad credentials"}
            if message == "Bad credentials":
                raise AuthentificationFailed(message)

            # {"errorCode": "RESOURCE_ACCESS_DENIED", "error": "Not authenticated"}
            if message == "Not authenticated":
                raise AuthentificationFailed(message)

            # {"error": "Server busy, please try again later. (Too many executions)"}
            if message == "Server busy, please try again later. (Too many executions)":
                raise CozytouchException(message)

            # {"error": "UNSUPPORTED_OPERATION", "error": "No such command : ..."}
            if "No such command" in message:
                raise CozytouchException(message)

            # {'errorCode': 'UNSPECIFIED_ERROR', 'error': 'Invalid event listener id : ...'}
            if "Invalid event listener id" in message:
                raise CozytouchException(message)

            # {'errorCode': 'UNSPECIFIED_ERROR', 'error': 'No registered event listener'}
            if message == "No registered event listener":
                raise CozytouchException(message)

        raise Exception(message if message else result)

    async def register_event_listener(self) -> str:
        """
        Register a new setup event listener on the current session and return a new
        listener id.
        Only one listener may be registered on a given session.
        Registering an new listener will invalidate the previous one if any.
        Note that registering an event listener drastically reduces the session
        timeout : listening sessions are expected to call the /events/{listenerId}/fetch
        API on a regular basis.
        """
        reponse = await self.__post("events/register")
        listener_id = reponse.get("id")
        self.event_listener_id = listener_id

        return listener_id

    async def unregister_event_listener(self) -> None:
        """
        Unregister an event listener.
        API response status is always 200, even on unknown listener ids.
        """
        await self.__post(f"events/{self.event_listener_id}/unregister")
        self.event_listener_id = None

    @backoff.on_exception(
        backoff.expo,
        (AuthentificationFailed, CozytouchException),
        max_tries=2,
        on_backoff=refresh_listener,
    )
    async def fetch_events(self):
        """
        Fetch new events from a registered event listener. Fetched events are removed
        from the listener buffer. Return an empty response if no event is available.
        Per-session rate-limit : 1 calls per 1 SECONDS period for this particular
        operation (polling)
        """
        response = await self.__post(f"events/{self.event_listener_id}/fetch")
        return response
