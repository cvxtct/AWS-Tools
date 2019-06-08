#!/usr/bin/env python3

"""Example Code for parse SSM parameters.
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


def get_parameter(param_name: object) -> object:
    """Return the result of the boto3 ssm clients response.
    :type param_name: object
    """
    try:
        session = boto3.session.Session(profile_name=PROFILE_NAME,
                                        region_name=REGION_NAME)
        ssm_client = session.client('ssm')
        parameter = ssm_client.get_parameter(
            Name=param_name, WithDecryption=True)
        return {
            'Name': parameter['Parameter']['Name'],
            'Value': parameter['Parameter']['Value'],
            'Version': parameter['Parameter']['Version'],
            'Modified': parameter['Parameter']['LastModifiedDate'],
            'Arn': parameter['Parameter']['ARN'],
        }
    except ParamValidationError as _e:
        _logger("Parameter validation error: %s" % _e)
    except ClientError as _e:
        _logger("Unexpected error: %s" % _e)


def get_parameters(res_type: object) -> dict:
    """Return the result of the boto3 ssm iterator clients response.
    get parameters, collect params which contain given string,
    put them into param_name list then call get_parameter() and
    put parameter value belongs to parameter_name
    :type res_type: object
    """
    session = boto3.session.Session(profile_name=PROFILE_NAME,
                                    region_name=REGION_NAME)
    ssm_client = session.client('ssm')
    paginator = ssm_client.get_paginator('describe_parameters')
    params = []
    param_name = []
    param_value = dict()

    for response in paginator.paginate():
        params.append(response['Parameters'])

    for iteration, _ in enumerate(params):
        for param_obj, _ in enumerate(params[iteration]):
            if res_type in params[iteration][param_obj]['Name']:
                param_name.append((params[iteration][param_obj]['Name']))

    for iteration, _ in enumerate(param_name):

        param_value.update({iteration: get_parameter(param_name[iteration])})


    return json.dumps(param_value["Items"], default=_converter, indent=4)

if __name__ == '__main__':

    PARAMS_SSM = get_parameters('cf')
    _logger(PARAMS_SSM)
