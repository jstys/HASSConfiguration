import json
import sys
from adapt.entity_tagger import EntityTagger
from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie
from adapt.intent import IntentBuilder
from adapt.parser import Parser
from adapt.engine import IntentDeterminationEngine
from intent_builders.intent_configuration import entity_json, translations

tokenizer = EnglishTokenizer()
trie = Trie()
tagger = EntityTagger(trie, tokenizer)
parser = Parser(tokenizer, tagger)
engine = IntentDeterminationEngine()

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
    .optionally("Percentage")\
    .optionally("MinVal")\
    .optionally("MaxVal")\
    .build())

intents.append(\
    IntentBuilder("PowerIntent")\
    .require("PowerVerb")\
    .optionally("AllModifier")\
    .optionally("Room")\
    .one_of("LightObject", "LampObject", "MediaObject", "InputName", "ACObject")\
    .optionally("Percentage")\
    .build())

intents.append(\
    IntentBuilder("MediaIntent")\
    .require("MediaVerb")\
    .optionally("AllModifier")\
    .optionally("Room")\
    .require("MediaObject")\
    .build())

intents.append(\
    IntentBuilder("ListIntent")\
    .one_of("ListItemAdd", "ListItemRemove", "ListGenerate")
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

intents.append(\
    IntentBuilder("ColorIntent")\
    .require("ModifyVerb")\
    .one_of("LightObject", "LampObject")\
    .require("Color")\
    .build())

intents.append(\
    IntentBuilder("ModeIntent")\
    .require("ModifyVerb")
    .one_of("LightObject", "LampObject")\
    .require("ModeName")\
    .build())

for intent in intents:
    engine.register_intent_parser(intent)

def massage_text(val):
    if isinstance(val, str):
        val = val.replace("'", "")
        if val in translations:
            val = translations.get(val)
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
