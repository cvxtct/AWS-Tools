#!/usr/bin/env python3

from __future__ import print_function
import json
import logging
import datetime
import boto3

session = boto3.session.Session(profile_name='dev')
iam = session.client('iam', region_name='eu-west-1')


def _logger(message: object) -> str:
    """Return log
    :type message: object
    """
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    return logging.info(message)


def _converter(_o: object) -> object:
    """Return str from datetime.
    :type _o: object
    """
    if isinstance(_o, datetime.datetime):
        return _o.__str__()
    return None


def get_users_list() -> object:
    """

    :rtype: object
    """
    users = []
    user_names = []
    paginator = iam.get_paginator('list_users')

    for response in paginator.paginate():
        users.append(response['Users'])

    for iteration in range(len(users)):
        for userobj in range(len(users[iteration])):
            user_names.append((users[iteration][userobj]['UserName']))

    return user_names


def list_access_key() -> object:
    """

    :rtype: object
    """
    access_keys = []
    usr_list = get_users_list()

    paginator = iam.get_paginator('list_access_keys')
    for usr in usr_list:
        for response in paginator.paginate(UserName=usr):
            access_keys.append(response['AccessKeyMetadata'])

    return json.dumps(access_keys, default=_converter, indent=4)


if __name__ == '__main__':

    _logger(len(iam.list_users()['Users']))

    USR = get_users_list()
    USR_KEY = list_access_key()

    _logger(USR_KEY)

