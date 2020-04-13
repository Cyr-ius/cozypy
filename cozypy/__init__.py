# -*- coding:utf-8 -*-
'''
Provides authentification and row access to Cozytouch modules.
'''
name = 'cozypy'
__version__ = '1.2.1'
__all__ = ['cozypy']

from .client import CozytouchClient
from .exception import CozytouchException
