#!/usr/bin/env python3

def mute_host(hostname, FOREVER=False, ENDHOURS=2, FORCE=False):
    # Initialize API for use and grab requestor
    dd_login = api_initialization(args.config)
    # Mute the host by hostname
    for host in hostname.split(','):
        if host == "":
            continue
        if FOREVER:
            try:
                if FORCE:
                    result = api.Host.mute(host,
                            message="scheduled by ddctl for {}".format(dd_login),
                            override=True)
                else:
                    result = api.Host.mute(host,
                            message="scheduled by ddctl for {}".format(dd_login))
            except Exception as err:
                raise SystemExit("Unable to mute {0} due to: {1}".format(host, err))
        else:
            try:
                if FORCE:
                    result = api.Host.mute(host, end=hours_from_now(ENDHOURS),
                            message="scheduled by ddctl for {}".format(dd_login),
                            override=True)
                else:
                    result = api.Host.mute(host, end=hours_from_now(ENDHOURS),
                            message="scheduled by ddctl for {}".format(dd_login))
            except Exception as err:
                raise SystemExit("Unable to mute {0} due to: {1}".format(host, err))
        # Print successful result
        try:
            print("{0} was {1}".format(result['hostname'], result['action']))
        except KeyError:
            print("NOTE: {0}".format(result['errors'][0].split('. ')[0] + '.'))

def unmute_host(hostname):
    # Initialize API for use and grab requestor
    dd_login = api_initialization(args.config)
    # Unmute the host by hostname
    for host in hostname.split(','):
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
