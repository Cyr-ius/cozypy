"""Cozytouch API."""
import asyncio
import datetime
import json
import logging
import re
import urllib.parse

import aiohttp

from .constant import API_THROTTLE, COZYTOUCH_ENDPOINTS, USER_AGENT
from .exception import (AuthentificationFailed, CozytouchException,
                        HttpRequestFailed, HttpTimeoutExpired)
from .handlers import Handler
from .utils import CozytouchEncoder

logger = logging.getLogger(__name__)


class CozytouchClient:
    """Client session."""

    def __init__(self, username, password, timeout=60, max_retry=3):
        """Initialize session."""
        self.cookies = None
        self.retry = 0
        self.max_retry = max_retry
        self.username = username
        self.password = password
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.is_connected = False
        self._devices_data = None
        self._devices_info = None
        self._last_fetch = None
        self._lock = asyncio.Lock()

    @classmethod
    def build_url(cls, resource, data):
        """Build url."""
        if resource not in COZYTOUCH_ENDPOINTS:
            raise CozytouchException(
                "Bad resource: {resource}".format(resource=resource)
            )
        url = COZYTOUCH_ENDPOINTS[resource]

        matches = re.findall("(?P<text>\\[(?P<param>[^] ]+)\\])", url)
        for text, key in matches:
            url = url.replace(text, urllib.parse.quote_plus(data[key]))

        return url

    async def __make_request(self, resource, method="GET", data=None, headers=None, json_encode=True):
        """Make call to Cozytouch API."""
        if not self.is_connected and resource != "login":
            raise AuthentificationFailed

        if data is None:
            data = {}

        if headers is None:
            headers = {}

        headers["User-Agent"] = USER_AGENT

        url = self.build_url(resource, data)
        logger.debug("Request %s : %s", method, resource)
        async with aiohttp.ClientSession(cookies=self.cookies, timeout=self.timeout) as session:
            if method == "GET":
                try:
                    async with session.get(url) as resp:
                        response_json = await resp.json()
                        response = resp
                except aiohttp.ClientError as error:
                    raise HttpRequestFailed("Error Request") from error
                except asyncio.TimeoutError as error:
                    raise HttpTimeoutExpired("Error Request") from error
            else:
                if json_encode:
                    data = json.dumps(data, cls=CozytouchEncoder)
                    headers["Content-Type"] = "application/json"

                try:
                    logger.debug("Json: %s", data)
                    async with session.post(url, headers=headers, data=data) as resp:
                        response_json = await resp.json()
                        response = resp
                except aiohttp.ClientError as error:
                    raise HttpRequestFailed("Error Request") from error
                except asyncio.TimeoutError as error:
                    raise HttpTimeoutExpired("Error Request") from error

        logger.debug("Response status : %s", response.status)
        logger.debug("Response json : %s", response_json)

        return response_json, response

    async def __make_request_reconnect(self, resource, method="GET", data=None, headers=None, json_encode=True):
        response_json, response = await self.__make_request(
            resource, method, data, headers, json_encode
        )
        if response.status == 401:
            logger.debug("Connection refused, reconnecting")
            await self.connect()
            response_json, response = await self.__make_request(
                resource, method, data, headers, json_encode
            )
        return response_json, response

    async def connect(self):
        """Authenticate using username and userPassword."""
        _, response = await self.__make_request(
            "login",
            method="POST",
            data={"userId": self.username, "userPassword": self.password},
            json_encode=False,
        )

        if response.status != 200:
            raise AuthentificationFailed(response.status)
        self.is_connected = True
        self.cookies = {"JSESSIONID": response.cookies.get("JSESSIONID")}

    async def get_setup(self):
        """Get cozytouch setup (devices, places)."""
        response_json, response = await self.__make_request_reconnect(
            "setup", method="GET"
        )
        if response.status != 200:
            raise CozytouchException(
                "Unable to retrieve setup: {error}[{code}]".format(
                    error=response_json["error"], code=response_json["errorCode"]
                )
            )
        return Handler(response_json, self)

    async def get_devices_data(self):
        """Fetch data."""
        async with self._lock:  # Prevent call to the API if there is already one running
            fresh = False
            if self._last_fetch is not None:
                fresh = (
                    datetime.datetime.now() - self._last_fetch
                ).total_seconds() < API_THROTTLE
            if self._devices_data is None or not fresh:
                if self._devices_data is None:
                    logger.debug("Cache not available, fetching datas")
                else:
                    delta = (datetime.datetime.now() - self._last_fetch).total_seconds()
                    logger.debug("Cache too old %s, fetching datas", delta)
                response_json, response = await self.__make_request_reconnect("devices")
                if response.status != 200:
                    raise CozytouchException(
                        "Unable to retrieve devices : {error}[{code}]".format(
                            error=response_json["error"],
                            code=response_json["errorCode"],
                        )
                    )
                self._devices_data = response_json
                self._last_fetch = datetime.datetime.now()
            else:
                logger.debug("Using cache for devices data")
        return self._devices_data

    async def get_devices(self):
        """Get all devices (devices, places)."""
        setup = await self.get_setup()
        return setup.devices

    async def get_devices_info(self):
        """Get all infos device."""
        self._devices_info = {}
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

    async def send_commands(self, commands):
        """Send command to device."""
        response_json, response = await self.__make_request_reconnect(
            "apply",
            method="POST",
            data=commands,
            headers={"Content-type": "application/json"},
        )
        if response.status != 200:
            raise CozytouchException(
                "Unable to send command : {error}[{code}]".format(
                    error=response_json["error"], code=response_json["errorCode"]
                )
            )
        return response_json
