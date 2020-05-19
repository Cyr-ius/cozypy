"""Cozytouch API."""
import logging
import json
import re
import aiohttp
import urllib.parse
import datetime
import asyncio

from .constant import USER_AGENT, COZYTOUCH_ENDPOINTS, API_THROTTLE
from .exception import CozytouchException, AuthentificationFailed, HttpRequestFailed
from .handlers import SetupHandler, DevicesHandler
from .utils import CozytouchEncoder

logger = logging.getLogger(__name__)


class CozytouchClient:
    """Client session."""

    def __init__(self, username, password, timeout=60, max_retry=3):
        """Initializate session."""
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

    async def __make_request(
        self, resource, method="GET", data=None, headers=None, json_encode=True
    ):
        """Make call to Cozytouch API."""
        if not self.is_connected and resource != "login":
            raise AuthentificationFailed

        if data is None:
            data = {}
        logger.debug("Request %s : %s", resource, data)
        if headers is None:
            headers = {}

        headers["User-Agent"] = USER_AGENT

        url = self.build_url(resource, data)
        async with aiohttp.ClientSession(
            cookies=self.cookies, timeout=self.timeout
        ) as session:
            if method == "GET":
                try:
                    async with session.get(url) as resp:
                        response_json = await resp.json()
                        response = resp
                except aiohttp.ClientError as e:
                    raise HttpRequestFailed("Error Request", e)
            else:
                if json_encode:
                    data = json.dumps(data, cls=CozytouchEncoder)
                    headers["Content-Type"] = "application/json"

                try:
                    async with session.post(url, headers=headers, data=data) as resp:
                        response_json = await resp.json()
                        response = resp
                except aiohttp.ClientError as e:
                    raise HttpRequestFailed("Error Request", e)
        logger.debug(f"Response status : {response.status}")
        return response_json, response

    async def __make_request_reconnect(
        self, resource, method="GET", data=None, headers=None, json_encode=True
    ):
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
        response_json, response = await self.__make_request(
            "login",
            method="POST",
            data={"userId": self.username, "userPassword": self.password},
            json_encode=False,
        )
        logger.debug(response.cookies)
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
        return SetupHandler(response_json, self)

    async def devices_data(self):
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
                    logger.debug(f"Cache too old {delta}, fetching datas")
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
        """.Get cozytouch setup (devices, places)."""
        data = await self.devices_data()
        return DevicesHandler(data, self)

    async def devices_info(self):
        """Get data using cache if available."""
        self._devices_info = {}
        data = await self.devices_data()
        for dev in data:
            metadata = SetupHandler.parse_url(dev["deviceURL"])
            self._devices_info[metadata.base_url] = dev
        return self._devices_info

    async def get_device_info(self, device_url):
        """Get cozytouch setup (devices, places)."""
        datas = await self.devices_info()

        if device_url not in datas:
            raise CozytouchException(
                "Unable to retrieve device {device_url}: not in available devices".format(
                    device_url=device_url
                )
            )
        return datas.get(device_url).get("states")

    async def send_commands(self, commands, *args):
        """Get devices states."""
        logger.debug("Request commands %s", str(commands))
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

        logger.debug("Response commands %s", response.content)
        return response_json
