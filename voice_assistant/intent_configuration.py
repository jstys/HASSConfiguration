translations = {
    "zip lock bags": "ziploc bags",
    "lampes": "lamps"
}

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
            "lamps"
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