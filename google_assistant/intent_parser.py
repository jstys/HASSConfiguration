__author__ = 'seanfitz'
"""
A sample program that uses multiple intents and disambiguates by
intent confidence

try with the following:
PYTHONPATH=. python examples/multi_intent_parser.py "what's the weather like in tokyo"
PYTHONPATH=. python examples/multi_intent_parser.py "play some music by the clash"
"""

import json
import sys
from adapt.entity_tagger import EntityTagger
from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie
from adapt.intent import IntentBuilder
from adapt.parser import Parser
from adapt.engine import IntentDeterminationEngine

tokenizer = EnglishTokenizer()
trie = Trie()
tagger = EntityTagger(trie, tokenizer)
parser = Parser(tokenizer, tagger)
engine = IntentDeterminationEngine()

entity_json = {
    "Normal":{
        "Room": [
            "living room",
            "bathroom",
            "kitchen",
            "garage",
            "bedroom",
            "office",
            "house"
        ],
        "LightObject": [
            "lights",
            "light"
        ],
        "LampObject": [
            "lamp",
            "lamps",
            "lampes"
        ],
        "MediaObject": [
            "TV"
        ],
        "LevelVerb": [
            "dim",
            "turn up",
            "turn down"
        ],
        "PowerVerb": [
            "turn on",
            "turn off"
        ],
        "VacuumObject": [
            "vacuum"
        ],
        "MediaVerb": [
            "mute",
            "pause",
            "resume",
            "stop",
            "start"
        ],
        "BroadcastVerb": [
            "broadcast",
            "announce"
        ],
        "TalkVerb": [
            "say",
            "tell"
        ],
        "ListVerb": [
            "add",
            "remove",
            "read"
        ],
        "ListType": [
            "to do",
            "to dos",
            "grocery",
            "groceries",
            "shopping"
        ],
        "AllModifier": [
            "all"
        ],
        "GoodnightVerb": [
            "good night",
            "nighty night",
            "commence bed time sequence"
        ]
    },
    "Regex": [
        "(?P<Percentage>[0-9]+%)",
        "add (?P<ListItemAdd>.*) to",
        "remove (?P<ListItemRemove>.*) from",
        "its (?P<SceneEvent>.*) time",
        "the (?P<InputName>.*) input",
        "the (?P<VacuumName>.*) vacuum"
    ]
}

for entity, values in entity_json['Normal'].items():
    for value in values:
        engine.register_entity(value, entity)

for regex_entity in entity_json['Regex']:
    engine.register_regex_entity(regex_entity)

intents = []

intents.append(\
    IntentBuilder("LevelIntent")\
    .require("LevelVerb")\
    .optionally("AllModifier")\
    .optionally("Room")\
    .one_of("LightObject", "LampObject", "MediaObject")\
    .require("Percentage")\
    .build())

intents.append(\
    IntentBuilder("PowerIntent")\
    .require("PowerVerb")\
    .optionally("AllModifier")\
    .optionally("Room")\
    .one_of("LightObject", "LampObject", "MediaObject", "InputName")\
    .optionally("Percentage")\
    .build())

intents.append(\
    IntentBuilder("MediaIntent")\
    .require("MediaVerb")\
    .optionally("AllModifier")\
    .optionally("Room")\
    .optionally("MediaObject")\
    .build())

intents.append(\
    IntentBuilder("ListIntent")\
    .one_of("ListItemAdd", "ListItemRemove")
    .require("ListType")\
    .build())

intents.append(\
    IntentBuilder("TalkIntent")\
    .require("TalkVerb")\
    .require("Room")\
    .build())

intents.append(\
    IntentBuilder("SceneIntent")\
    .require("SceneEvent")\
    .build())

intents.append(\
    IntentBuilder("GoodnightCommand")\
    .require("GoodnightVerb")\
    .build())

intents.append(\
    IntentBuilder("VacuumIntent")\
    .require("MediaVerb")\
    .optionally("VacuumName")
    .require("VacuumObject")\
    .build())

for intent in intents:
    engine.register_intent_parser(intent)

def massage_text(val):
    if isinstance(val, str):
        val = val.replace("'", "")
        return val
    else:
        return val

def massage_json(json_val):
    massaged_json = {}
    for key, val in json_val.items():
        massaged_json[massage_text(key)] = massage_text(val)

    return massaged_json

def parse_intent(val):
    val = massage_text(val)
    results = engine.determine_intent(val)
    for obj in results:
        if obj is not None and obj.get('confidence') > 0:
            return (massage_json(obj), val)
    return (None, val)


if __name__ == "__main__":
    raw = ' '.join(sys.argv[1:])
    intent, text = parse_intent(raw)
    if intent is not None:
        intent['raw'] = text
        print(json.dumps(intent, indent=4))
