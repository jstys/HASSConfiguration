#!/srv/homeassistant/bin/python3
import json
import sys
import homeassistant.remote as remote

api = remote.API('127.0.0.1')

def tts_say(message):
    remote.call_service(api, "script", "snips_voice", {"message": message})

if __name__ == '__main__':
    raw_payload = sys.argv[1]
    json_payload = {}
    try:
        json_payload = json.loads(raw_payload)
    except:
        tts_say("Unable to parse intent")
        sys.exit(1)

    tts_say("Successfully parsed intent")
