#!/usr/bin/env python3
from brain.connector import dd_api_init
from datadog import api
from brain.utils import hours_from_now

# Initialize API for use and grab requestor
dd_login = dd_api_init()

def mute_host(hostname, FOREVER=False, ENDHOURS=2, FORCE=False):
    # Mute the host by hostname
    for host in hostname:
        if host == "":
            continue
        if FOREVER:
            try:
                if FORCE:
                    result = api.Host.mute(host,
                            message="scheduled by ddctl for {}".format(dd_login['user']),
                            override=True)
                else:
                    result = api.Host.mute(host,
                            message="scheduled by ddctl for {}".format(dd_login['user']))
            except Exception as err:
                raise SystemExit("Unable to mute {0} due to: {1}".format(host, err))
        else:
            try:
                if FORCE:
                    result = api.Host.mute(host, end=hours_from_now(ENDHOURS),
                            message="scheduled by ddctl for {}".format(dd_login['user']),
                            override=True)
                else:
                    result = api.Host.mute(host, end=hours_from_now(ENDHOURS),
                            message="scheduled by ddctl for {}".format(dd_login['user']))
            except Exception as err:
                raise SystemExit("Unable to mute {0} due to: {1}".format(host, err))
        # Print successful result
        try:
            print("{0} was {1}".format(result['hostname'], result['action']))
        except KeyError:
            print("NOTE: {0}".format(result['errors'][0].split('. ')[0] + '.'))

def unmute_host(hostname):
    # Unmute the host by hostname
    for host in hostname:
        if host == "":
            continue
        try:
            result = api.Host.unmute(host)
        except Exception as err:
            raise SystemExit("Unable to unmute {0} due to: {1}".format(host, err))
        # Print successful result
        try:
            print("{0} was {1}".format(result['hostname'], result['action']))
        except KeyError:
            print("NOTE: {0}".format(result['errors'][0]))
