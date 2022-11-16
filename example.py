#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This example can be run safely as it won't change anything in your box configuration."""
import asyncio
import logging

from cozytouchpy import CozytouchClient
from cozytouchpy.exception import CozytouchException

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

username = "my-username"
password = "my-password"

client = CozytouchClient(username, password, "atlantic_cozytouch")


async def async_demo():
    """Cozytouch demonstration."""

    def device_info(device):
        logger.info("\t Name:{}".format(device.name))
        logger.info("\t Build:{}".format(device.build))
        logger.info("\t Client:{}".format(device.client))
        logger.info("\t Creation Time:{}".format(device.creationTime))
        logger.info("\t Device url:{}".format(device.deviceUrl))
        logger.info("\t\t Id:{}".format(device.id))
        logger.info("\t\t Place:{}".format(device.place.name))
        logger.info("\t\t Suported states:")
        for state in device.supported_states:
            logger.info("\t\t\t {}".format(state))
        logger.info("\t\t States value:")
        for state in device.supported_states:
            logger.info("\t\t\t {} {}".format(state.value, device.get_state(state)))
        logger.info("\t\t Is on: {}".format(device.is_on))
        if hasattr(device, "operating_mode"):
            logger.info("\t\t Operating mode:{}".format(device.operating_mode))
        if hasattr(device, "sensors") and len(device.sensors) > 0:
            logger.info("\t\t Sensors")
            for sensor in device.sensors:
                logger.info("\t\t\t Id:{}".format(sensor.id))
                logger.info("\t\t\t Name:{}".format(sensor.name))
                logger.info("\t\t\t Type: {}".format(sensor.widget))
                for sensor_state in sensor.states:
                    logger.info(
                        "\t\t\t\t {name}: {value}".format(
                            name=sensor_state["name"], value=sensor_state["value"]
                        )
                    )

    try:
        await client.connect()
        setup = await client.get_setup()
    except CozytouchException as e:
        logger.error(e)

    logger.info("### PLACES ###")
    for place in setup.places:
        logger.info(place.id)
        logger.info(place.name)

    logger.info("### BOILERS ###")
    for boiler in setup.boilers:
        logger.info(boiler.id)
        device_info(boiler)

    logger.info("### WATER HEATERS ###")
    for water_heater in setup.water_heaters:
        logger.info(water_heater.id)
        device_info(water_heater)

    logger.info("### HEATERS ###")
    for heater in setup.heaters:
        logger.info(heater.id)
        device_info(heater)

    logger.info("### PODS ###")
    for pod in setup.pods:
        logger.info(pod.id)
        device_info(pod)

    logger.info("### GATEWAYS ###")
    for gw in setup.gateways:
        logger.debug(gw.id)
        logger.debug(gw.gatewayId)
        logger.debug(gw.is_on)
        logger.debug(gw.version)
        logger.debug(gw.status)


loop = asyncio.get_event_loop()
loop.run_until_complete(async_demo())
loop.close()
