#!/usr/bin/env python3
from datadog import initialize, api
from configparser import ConfigParser
import argparse

def api_initialization(config_file):
    # Pulling in API and APP Token
    try:
        config = ConfigParser()
        config.read(config_file)
        #config.read('ddctl.conf')
        api_key = config['ddctl']['api_key']
        app_key = config['ddctl']['app_key']
    except Exception as err:
        raise SystemExit('There was an issue reading the config file.')

    # Initialize the connection
    options = {'api_key': api_key, 'app_key': app_key}
    try:
        initialize(**options)
    except Exception as err:
        raise SystemExit('Unable to initialize due to: {}'.format(err))

def mute_host(hostname):
    # Mute the host by hostname
    try:
        result = api.Host.mute(hostname)
    except Exception as err:
        raise SystemExit('Unable to mute {0} due to: {1}'.format(hostname, err))
    # Print successful result
    try:
        print("{0} was {1}".format(result['hostname'], result['action']))
    except KeyError:
        print("NOTE: {0}".format(result['errors'][0].split('. ')[0] + '.'))

def unmute_host(hostname):
    # Unmute the host by hostname
    try:
        result = api.Host.unmute(hostname)
    except Exception as err:
        raise SystemExit('Unable to unmute {0} due to: {1}'.format(hostname, err))
    # Print successful result
    try:
        print("{0} was {1}".format(result['hostname'], result['action']))
    except KeyError:
        print("NOTE: {0}".format(result['errors'][0]))

def search_for_host(query):
    # Search for host by keywords
    try:
        result = api.Infrastructure.search(q='hosts:{0}'.format(query))
    except Exception as err:
        raise SystemExit('Unable to complete query {0} due to: {1}'.format(query, err))
    # Print successful result
    print("Found the following based on your query of {0}:".format(query))
    for host in result['results']['hosts']:
        print(host)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--config",
                        help="declare path to your ddctl.conf config file",
                        metavar="FILE", default="ddctl.conf")
    parser.add_argument("--query",
                        help="query datadog for a list of hosts by query",
                        default="_empty_")
    parser.add_argument("--host", help="hostname to mute or unmute",
                        default="_empty_")
    parser.add_argument("--mute", action="store_true",
                        help="mute host and schedule downtime",
                        default="_empty_")
    parser.add_argument("--unmute", action="store_true",
                        help="UNmute host and return to normal monitoring",
                        default="_empty_")
    args = parser.parse_args()

    if not args.query == "_empty_":
        api_initialization(args.config)
        search_for_host(args.config)

    if not args.mute == "_empty_":
        if args.host == "_empty_":
            raise SystemExit("mute argument requires a host argument")
        api_initialization(args.config)
        mute_host(args.host)

    if not args.unmute == "_empty_":
        if args.host == "_empty_":
            raise SystemExit("unmute argument requires a host argument")
        api_initialization(args.config)
        unmute_host(args.host)
