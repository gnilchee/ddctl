#!/usr/bin/env python3
from brain.connector import dd_api_init
from datadog import api
from brain.utils import hours_from_now

# Initialize API for use and grab requestor
dd_login = dd_api_init()

def create_downtime(scope, FOREVER=False, ENDHOURS=2):
    # Create downtime
    if FOREVER:
        try:
            result = api.Downtime.create(scope=scope, message="scheduled by ddctl for {}".format(dd_login['user']))
            if not result['active']:
                raise SystemExit("I don't show the downtime as active. Please investigate.")
            else:
                print("Downtime was successfully scheduled that will be in place until removed.")
        except Exception as err:
            raise SystemExit("There was an error adding downtimes: {0}".format(err))
    else:
        try:
            result = api.Downtime.create(scope=scope, end=hours_from_now(ENDHOURS), message="scheduled by ddctl for {}".format(dd_login['user']))
            if not result['active']:
                raise SystemExit("I don't show the downtime as active. Please investigate.")
            else:
                print("Downtime was successfully scheduled.")
        except Exception as err:
            raise SystemExit("There was an error adding downtimes: {0}".format(err))

def get_downtimes(MY_DOWNTIMES=False, ALL_DOWNTIMES=False):
    # List downtimes owned by you
    if MY_DOWNTIMES and not ALL_DOWNTIMES:
        try:
            result = api.Downtime.get_all(current_only=True)
        except Exception as err:
            raise SystemExit("Unable to get your downtimes due to: {0}".format(err))
        print("Downtimes created by {}:".format(dd_login['user']))
        count = 0
        for downtime in result:
            if downtime['message'] is not None \
                and downtime['message'].split()[-1] == dd_login['user']:
                count += 1
                print("Scope: '{scope}' has id: {id}"
                    .format(scope=downtime['scope'],
                    id=downtime['id']))
        if count == 0:
            print("None.")
    # Get all downtimes
    if ALL_DOWNTIMES and not MY_DOWNTIMES:
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
            print("There are no current downtimes.")
            raise SystemExit(0)

def remove_downtime(id):
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
        raise SystemExit("Ran into an issue confirming downtime delete was successful: {err}".format(err=err))

def remove_downtimes_by_scope(scope):
    # Grab the current downtimes
    try:
        api_response = api.Downtime.get_all(current_only=True)
    except Exception as err:
        raise SystemExit("Issue grabbing all current downtimes: {err}".format(err=err))
    # Create two lists for work
    response_list = []
    scope_match_list = []
    # Lets do this
    for resp in api_response:
        response_list.append({'id': resp['id'], 'scope': resp['scope']})
    # Comparing scope lists using sets
    for item in response_list:
        if set(scope) == set(item['scope']):
            scope_match_list.append(item)
    if len(scope_match_list) < 1:
        raise SystemExit("There were no exact scope matches.")
    elif len(scope_match_list) > 1:
        raise SystemExit("There were multiple matches, try removing by id.")
    elif len(scope_match_list) == 1:
        # Delete downtime by scope
        scope_id = scope_match_list[0]['id']
        try:
            api.Downtime.delete(scope_id)
        except Exception as err:
            raise SystemExit("Ran into an issue removing downtime by scope: {err}".format(err=err))
        # Confirm the downtime was deleted
        try:
            result = api.Downtime.get(scope_id)
            if result['active']:
                raise SystemExit("ERROR: I still show the downtime as active for your scope.")
            else:
                print("Downtime monitor delete request was successful.")
        except Exception as err:
            raise SystemExit("Ran into an issue confirming downtime delete was successful: {err}".format(err=err))
