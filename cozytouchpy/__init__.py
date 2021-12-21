# -*- coding:utf-8 -*-
"""Provides authentification and row access to Cozytouch modules."""
from .client import CozytouchClient
from .exception import AuthentificationFailed, CozytouchException, HttpRequestFailed, HttpTimeoutExpired

name = "cozytouchpy"
__version__ = "3.6"
__all__ = [
    "CozytouchClient",
    "AuthentificationFailed",
    "CozytouchException",
    "HttpRequestFailed",
    "HttpTimeoutExpired",
]
