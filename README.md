# ddctl - Simple Datadog Control
#### Requirements
* `pip install -r requirements.txt`
* API and APP key from Datadog

#### Setup config for Datadog API
* Create a Datadog API credentials file and structure it like this:
~~~~
[ddctl]
api_key  = 9775a026f1ca7d1c6c5af9d94d9595a4
app_key  = 87ce4a24b5553d2e482ea8a8500e71b8ad4554ff
dd_login = user@example.com
~~~~
*This is a dummy API and APP key used in Datadog API documentation*
* Feel free to use `ddctl.credentials.example` as your template

* ddctl expects this file to be name `credentials` and located in your home directory in a hidden folder called `.ddctl`
  * For example: `/home/username/.ddctl/credentials`

#### Helper
```
ddctl - the simple Datadog Control command line utility

Usage:
  ddctl mute <host>... [--forever | --hours=<hrs>] [--force]
  ddctl unmute <host>...
  ddctl downtime remove <id>
  ddctl downtime set <scope>... [--forever | --hours=<hrs>]
  ddctl downtime list (mine|all)
  ddctl query host <query>
  ddctl query tags [--all|--by-host=<host>]
  ddctl (-h | --help)
  ddctl --version

Options:
  -h --help     Show this screen.
  --version     Show version.
```

#### Current Features
* Mute and Unmute by hostname
* List all current downtimes or by you
* Remove or Add downtimes by scope (tags)
* Query Datadog for list of host that can be muted
* Query Datadog for tags by hostname or all

#### TODO
* Get a dictionary of all monitor id and friendly name and reference that rather than calling Datadog everytime we make a call for for a list of downtimes.
* Be able to safely remove downtimes by scope.
  * Should be able to compare the scope as a set of two sets in the input scope and downtime scope.
* General cleanup of the code.
