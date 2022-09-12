from util.entity_map import name_map
from util import hassutil
from util import logger

class DoorLockAction():
    def __init__(self):
        self._locks = []

    def add_locks(self, locks):
        for lock in locks:
            self.add_lock(lock)

        return self

    def add_lock(self, lock):
        if lock in name_map:
            self._locks.append(hassutil.Entity(name_map[lock]))
        else:
            logger.error("Unable to add unknown lock to DoorLockAction: {}".format(lock))

        return self

    def lock(self):
        for lock in self._locks:
            hassutil.lock(lock)
            
    def unlock(self):
        for lock in self._locks:
            hassutil.unlock(lock)