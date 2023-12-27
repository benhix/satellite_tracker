from PySide6.QtCore import QThread, Signal, Slot
from time import sleep
import satellite_api

class TrackerWorker(QThread):
    update_signal = Signal(dict)

    def __init__(self, sat_id, observer_lat, observer_long):
        super().__init__()
        self.sat_id = sat_id
        self.observer_lat = observer_lat
        self.observer_long = observer_long
        self.running = True

    def run(self):
        while self.running:
            data = satellite_api.get_satellite_position(self.sat_id, self.observer_lat, self.observer_long)
            self.update_signal.emit(data)
            sleep(1)

    def stop(self):
        self.running = False