#!/srv/homeassistant/bin/python3
import sys
import homeassistant.remote as remote

api = remote.API('127.0.0.1')

remote.call_service(api, "script", sys.argv[1])
