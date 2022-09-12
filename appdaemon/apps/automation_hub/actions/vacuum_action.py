from util import hassutil
from util import logger
from util.entity_map import name_map

class VacuumAction():
    def __init__(self):
        self._vacuums = []
        
    def add_vacuums(self, vacuums):
        for vacuum in vacuums:
            self.add_vacuum(vacuum)
            
        return self
        
    def add_vacuum(self, vacuum):
        if vacuum in name_map:
            self._vacuums.append(hassutil.Entity(name_map[vacuum]))
        else:
            logger.error("Unable to add unknown light to VacuumAction: {}".format(vacuum))
            
        return self
        
    def start(self):
        for vacuum in self._vacuums:
            hassutil.call_service("vacuum", "start", entity_id=vacuum.entity_id)
    
    def pause(self):
        for vacuum in self._vacuums:
            hassutil.call_service("vacuum", "pause", entity_id=vacuum.entity_id)
    
    def stop(self):
        for vacuum in self._vacuums:
            hassutil.call_service("vacuum", "stop", entity_id=vacuum.entity_id)
    
    def return_home(self):
        for vacuum in self._vacuums:
            hassutil.call_service("vacuum", "return_to_base", entity_id=vacuum.entity_id)
    
    def locate(self):
        for vacuum in self._vacuums:
            hassutil.call_service("vacuum", "locate", entity_id=vacuum.entity_id)