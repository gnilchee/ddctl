#!/usr/bin/env python3

def search_for_host(query, CSV=False):
    # Initialize API for use
    dd_login = api_initialization(args.config)
    # Search for host by keywords
    try:
        result = api.Infrastructure.search(q='hosts:{0}'.format(query))
    except Exception as err:
        raise SystemExit("Unable to complete query {0} due to: {1}".format(query, err))
    # Print successful result
    if args.csv:
        CSV=True
    if CSV and len(result['results']['hosts']) > 1:
        print(",".join(sorted(result['results']['hosts'])))
    else:
        for host in sorted(result['results']['hosts']):
            print(host)

def get_all_tags():
    # Initialize API for use
    dd_login = api_initialization(args.config)
    # Return all tags in environment in json blob
    try:
        result = api.Tag.get_all()
        for tag in sorted(result['tags']):
            print(tag)
    except Exception as err:
        raise SystemExit("Unable to get all tags due to: {0}".format(err))

def get_tags_by_host(host):
    # Initialize API for use
    dd_login = api_initialization(args.config)
    # Return all tags in environment in json blob
    try:
        result = api.Tag.get(host)
        for tag in sorted(result['tags']):
            print(tag)
    except Exception as err:
        raise SystemExit("Unable to get tags for host {0} due to: {1}".format(host, err))
