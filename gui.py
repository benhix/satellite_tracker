import geocoder
from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QCheckBox
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Slot
import satellite_api
from location import draw_on_map
from time import sleep
from live_track import TrackerWorker

# Get current location
g = geocoder.ip('me')

observer_lat = g.latlng[0]
observer_long = g.latlng[1]
iss_id = '25544'

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Satellite Tracker")
        self.setup_ui()

    def setup_ui(self):
        # Set up your UI components here
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Background label
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 1920, 1080)
        self.bg_img = QPixmap('assets/star_background2.jpg')
        self.background.setStyleSheet("border: none;")

        # Map
        self.world_map = QLabel(self)
        self.world_map.setGeometry(0, -2, 1732, 866)
        self.pic = QPixmap('assets/map_2_1.jpg')
        self.world_map.setPixmap(self.pic)

        # Output text box
        self.right_box = QLabel(self)
        self.right_box.setGeometry(0, 840, 1734, 200)
        self.right_box.setStyleSheet("color: black;")

        font = QFont('New York', 18)
        #font.setPointSize(15)
        self.right_box.setFont(font)
        
        # Search Button
        self.confirm_button = QPushButton('Search', self)
        self.confirm_button.setGeometry(1738, 180, 180, 50)
        self.confirm_button.clicked.connect(self.on_click_update_map)

        # Live Track Button
        self.live_track_button = QPushButton('Live Track', self)
        self.live_track_button.setGeometry(1738, 250, 180, 50)
        self.live_track_button.clicked.connect(self.on_click_live_track)

        # Norad ID text edit
        self.norad_id = QLineEdit(self)
        self.norad_id.setGeometry(1738, 120, 180, 50)
        self.norad_id.setPlaceholderText("NORAD ID")

        # Link to NORAD ID list
        

        # Checkbox for live track
        self.live_track = QCheckBox()
        self.live_track.setGeometry(900, 100, 10, 10)
        

    def on_click_update_map(self):
        # Stop any existing thread
        if hasattr(self, 'tracker_thread') and self.tracker_thread.isRunning():
            self.tracker_thread.stop()
            self.tracker_thread.wait()

        self.iss_id = self.norad_id.text()
        data = satellite_api.get_satellite_position(self.iss_id, observer_lat, observer_long)

        first_position = data['positions'][0] if data['positions'] else None
        if first_position:
            sat_lat = first_position['satlatitude']
            sat_long = first_position['satlongitude']

            # Prepare the satellite information string
            satellite_str = f"   Name: {data['info']['satname']}"
            for position in data['positions']:
                satellite_str += f"\n   Latitude: {position['satlatitude']}   Longitude: {position['satlongitude']}\n"

            # Update the satellite information label
            self.right_box.setText(satellite_str)

            # Draw satellite on map and update
            new_map_pixmap = draw_on_map(sat_lat, sat_long) 
            self.world_map.setPixmap(new_map_pixmap)
        else:
            print("No position data available.")



    def on_click_live_track(self):
        self.iss_id = self.norad_id.text()

        # Stop any existing thread
        if hasattr(self, 'tracker_thread') and self.tracker_thread.isRunning():
            self.tracker_thread.stop()
            self.tracker_thread.wait()

        # Create and start the new tracking thread
        self.tracker_thread = TrackerWorker(self.iss_id, observer_lat, observer_long)
        self.tracker_thread.update_signal.connect(self.update_ui)
        self.tracker_thread.start() 

    @Slot(dict)
    def update_ui(self, data):
        first_position = data['positions'][0] if data['positions'] else None
        if first_position:
            sat_lat = first_position['satlatitude']
            sat_long = first_position['satlongitude']

            # Prepare the satellite information string
            satellite_str = f"   Name: {data['info']['satname']}"
            for position in data['positions']:
                satellite_str += f"\n   Latitude: {position['satlatitude']}   Longitude: {position['satlongitude']}\n"

            # Update the satellite information label
            self.right_box.setText(satellite_str)

            # Draw satellite on map and update
            new_map_pixmap = draw_on_map(sat_lat, sat_long)
            self.world_map.setPixmap(new_map_pixmap)
        else:
            print("No position data available.")

    def closeEvent(self, event):
        # Stop the tracker thread safely before closing the window
        if hasattr(self, 'tracker_thread') and self.tracker_thread.isRunning():
            self.tracker_thread.stop()
            self.tracker_thread.wait()  # Wait for the thread to finish
        event.accept()  # Accept the close event
