import requests
import hassutil
from requests_oauthlib import OAuth1

def _load_auth():
    secrets = hassutil.read_config_file(hassutil.SECRETS)
    if secrets:
        try:
            return OAuth1(secrets['trello_key'], secrets['trello_secret'], secrets['trello_oauth'])
        except KeyError:
            pass

    return None

