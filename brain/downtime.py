#!/usr/bin/env python3

def create_downtime(scope, FOREVER=False, ENDHOURS=2):
    # Initialize API for use and grab requestor
    dd_login = api_initialization(args.config)
    # Check arguments
    if args.forever:
        FOREVER=True
    if args.hours is not 2:
        ENDHOURS=args.hours
    # Create downtime
    if FOREVER:
        try:
            result = api.Downtime.create(scope=scope, message="scheduled by ddctl for {}".format(dd_login))
            if not result['active']:
                raise SystemExit("I don't show the downtime as active. Please investigate.")
            else:
                print("Downtime was successfully scheduled that will be in place until removed.")
        except Exception as err:
            raise SystemExit("There was an error adding downtimes: {0}".format(err))
    else:
        try:
            result = api.Downtime.create(scope=scope, end=hours_from_now(ENDHOURS), message="scheduled by ddctl for {}".format(dd_login))
            if not result['active']:
                raise SystemExit("I don't show the downtime as active. Please investigate.")
            else:
                print("Downtime was successfully scheduled.")
        except Exception as err:
            raise SystemExit("There was an error adding downtimes: {0}".format(err))

def get_downtimes():
    # Initialize API for use and grab requestor
    dd_login = api_initialization(args.config)
    # List downtimes owned by you
    if args.list_my_downtimes and args.list_all_downtimes == "_empty_":
        try:
            result = api.Downtime.get_all(current_only=True)
        except Exception as err:
            raise SystemExit("Unable to get your downtimes due to: {0}".format(err))
        print("Downtimes created by {}:".format(dd_login))
        count = 0
        for downtime in result:
            if downtime['message'] is not None \
                and downtime['message'].split()[-1] == dd_login:
                count += 1
                print("Scope: '{scope}' has id: {id}"
                    .format(scope=downtime['scope'],
                    id=downtime['id']))
        if count == 0:
            print("None.")
    # Get all downtimes
    if args.list_all_downtimes and args.list_my_downtimes == "_empty_":
        try:
            result = api.Downtime.get_all(current_only=True)
        except Exception as err:
            raise SystemExit("Unable to get all downtimes due to: {0}".format(err))
        if len(result) > 0:
            for downtime in result:
                print("Scope: '{scope}', Monitor: '{mon}' has id: {id}"
                    .format(scope=downtime['scope'],
                    mon="-" if downtime['monitor_id'] is None else \
                        api.Monitor.get(downtime['monitor_id'])['name'],
                    id=downtime['id']))
        else:
            print("There are no current downtimes.".format(dd_login))
            raise SystemExit(0)

def remove_downtime(id):
    # Initialize API for use and grab requestor
    dd_login = api_initialization(args.config)
    # Delete the downtime
    try:
        api.Downtime.delete(id)
    except Exception as err:
        raise SystemExit("Ran into an issue removing downtime '{id}': {err}".format(id=id, err=err))
    # Confirm the downtime was deleted
    try:
        result = api.Downtime.get(id)
        if result['active']:
            raise SystemExit("ERROR: I still show the downtime as active for {id}.".format(id=id))
        else:
            print("Downtime monitor delete request was successful.")
    except Exception as err:
        raise SystemExit("Ran into an issue confirming downtime delete was successful: {err}".format(id=id, err=err))
