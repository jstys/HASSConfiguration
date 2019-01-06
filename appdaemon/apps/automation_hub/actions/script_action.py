from util.entity_map import name_map
from util import hassutil

class ScriptAction():
    def __init__(self):
        self._scripts = []

    def add_scripts(self, scripts):
        self._scripts.extend(scripts)
        return self

    def add_script(self, script):
        self._scripts.append(script)
        return self

    def run(self):
        for script in self._scripts:
            hassutil.call_service("script", script)