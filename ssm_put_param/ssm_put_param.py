#!/usr/bin/env python3

"""Example Code for put parameters into SSM.
   Parameter naming convention: dev/cf/cognito/userPoolId
"""

from __future__ import print_function
import datetime
import logging
import json
import configparser
import boto3
from botocore.exceptions import ClientError, ParamValidationError


CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')
PROFILE_NAME = CONFIG['GLOBAL']['PROFILE_NAME']
REGION_NAME = CONFIG['GLOBAL']['REGION_NAME']


def _logger(message: object) -> str:
    """Return log
    :type message: object
    """
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        level=logging.INFO)
    return logging.info(message)


def _converter(_o: object) -> str:
    """Return str from datetime.
    :type _o: object
    """
    if isinstance(_o, datetime.datetime):
        return _o.__str__()
    return None


def _put_parameter() -> object:
    # TODO implement put parameter (batch)
    return None

