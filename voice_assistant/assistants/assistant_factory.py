import google_assistant.GoogleAssistant as GoogleAssistant

GOOGLE_ASSISTANT_TYPE = "google"
SNIPS_ASSISTANT_TYPE = "snips"

def create_assistant(assistant_type, assistant_config, hotword_detected, intent_built):
    if assistant_type == GOOGLE_ASSISTANT_TYPE:
        return create_google_assistant(assistant_config, hotword_detected, intent_built)
    else:
        return None

def create_google_assistant(assistant_config, hotword_detected, intent_built):
    assistant = GoogleAssistant(assistant_config, hotword_detected, intent_built)
    if assistant.validate_config():
        return assistant
    else:
        return None

def create_snips_assistant(assistant_config, hotword_detected, intent_built):
    return None