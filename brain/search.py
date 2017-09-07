#!/usr/bin/env python3
from brain.connector import dd_api_init
from datadog import api

# Initialize API for use
dd_login = dd_api_init()

def search_for_host(query):
    # Search for host by keywords
    try:
        result = api.Infrastructure.search(q='hosts:{0}'.format(query))
    except Exception as err:
        raise SystemExit("Unable to complete query {0} due to: {1}".format(query, err))
    # Print successful result
    for host in sorted(result['results']['hosts']):
        print(host)

def get_all_tags():
    # Return all tags in environment in json blob
    try:
        result = api.Tag.get_all()
        for tag in sorted(result['tags']):
            print(tag)
    except Exception as err:
        raise SystemExit("Unable to get all tags due to: {0}".format(err))

def get_tags_by_host(host):
    # Return all tags in environment in json blob
    try:
        result = api.Tag.get(host)
        for tag in sorted(result['tags']):
            print(tag)
    except Exception as err:
        raise SystemExit("Unable to get tags for host {0} due to: {1}".format(host, err))
