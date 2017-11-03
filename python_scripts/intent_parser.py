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

room_keywords = [
    "living room",
    "bathroom",
    "kitchen",
    "garage",
    "bedroom",
    "office",
    "house"
]

dimmable_objects = [
    "lights",
    "light",
    "lamp",
    "lampes",
    "lamps"
]

powerable_objects = [
    "lights",
    "light",
    "lamp",
    "lampes",
    "lamps",
    "TV"
]

media_objects = [
    "TV",
    "speaker",
    "chromecast"
]

brightness_verbs = [
    "dim",
    "brighten"
]

power_verbs = [
    "turn on",
    "turn off"
]

media_verbs = [
    "mute",
    "resume",
    "pause"
]

broadcast_verbs = [
    "broadcast",
    "announce"
]

talk_verbs = [
    "say",
    "tell"
]

list_verbs = [
    "add",
    "remove",
    "read"
]

list_types = [
    "to do",
    "to dos",
    "grocery",
    "groceries",
    "shopping"
]

engine.register_entity("all", "AllModifier")
engine.register_regex_entity("(?P<Percentage>[0-9]+%)")
engine.register_regex_entity("add (?P<ListItemAdd>.*) to")
engine.register_regex_entity("remove (?P<ListItemRemove>.*) from")
engine.register_regex_entity("its (?P<SceneEvent>.*) time")

for verb in talk_verbs:
    engine.register_entity(verb, "TalkVerb")

for verb in list_verbs:
    engine.register_entity(verb, "ListVerb")

for list_type in list_types:
    engine.register_entity(list_type, "ListType")

for room in room_keywords:
    engine.register_entity(room, "Room")

for verb in media_verbs:
    engine.register_entity(verb, "MediaVerb")

for verb in power_verbs:
    engine.register_entity(verb, "PowerVerb")

for power_object in powerable_objects:
    engine.register_entity(power_object, "PowerableObject")

for verb in brightness_verbs:
    engine.register_entity(verb, "BrightnessVerb")

for brightness_object in dimmable_objects:
    engine.register_entity(brightness_object, "DimmableObject")

for verb in broadcast_verbs:
    engine.register_entity(verb, "BroadcastVerb")

for media_object in media_objects:
    engine.register_entity(media_object, "MediaObject")

for verb in media_verbs:
    engine.register_entity(verb, "MediaVerb")

brightness_intent = IntentBuilder("BrightnessIntent")\
    .require("BrightnessVerb")\
    .optionally("AllModifier")\
    .optionally("Room")\
    .require("DimmableObject")\
    .require("Percentage")\
    .build()

power_intent = IntentBuilder("PowerIntent")\
    .require("PowerVerb")\
    .optionally("AllModifier")\
    .optionally("Room")\
    .require("PowerableObject")\
    .optionally("Percentage")\
    .build()

broadcast_intent = IntentBuilder("BroadcastIntent")\
    .require("BroadcastVerb")\
    .build()

media_intent = IntentBuilder("MediaIntent")\
    .require("MediaVerb")\
    .optionally("AllModifier")\
    .optionally("Room")\
    .optionally("MediaObject")\
    .build()

list_intent = IntentBuilder("ListIntent")\
    .require("ListVerb")\
    .optionally("ListItemAdd")\
    .optionally("ListItemRemove")\
    .require("ListType")\
    .build()

talk_intent = IntentBuilder("TalkIntent")\
    .require("TalkVerb")\
    .optionally("Room")\
    .build()

scene_intent = IntentBuilder("SceneIntent")\
    .require("SceneEvent")\
    .build()

engine.register_intent_parser(broadcast_intent)
engine.register_intent_parser(power_intent)
engine.register_intent_parser(brightness_intent)
engine.register_intent_parser(media_intent)
engine.register_intent_parser(list_intent)
engine.register_intent_parser(talk_intent)
engine.register_intent_parser(scene_intent)

def massage_text(val):
    if isinstance(val, str):
        val = val.replace("'", "")
        return val
    else:
        return val

def massage_json(json_val):
    massaged_json = {}
    for key, value in json_val.items():
        massaged_json[massage_text(key)] = massage_text(value)

    return massaged_json

def parse_intent(val):
    val = massage_text(val)
    intents = engine.determine_intent(val)
    for obj in intents:
        if obj is not None and obj.get('confidence') > 0:
            return (massage_json(obj), val)
    return (None, val)


if __name__ == "__main__":
    raw = ' '.join(sys.argv[1:])
    intent, text = parse_intent(raw)
    if intent is not None:
        intent['raw'] = text
        print(json.dumps(intent, indent=4))
