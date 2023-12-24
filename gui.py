import geocoder
from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit
from PySide6.QtGui import QPixmap
import satellite_api
from location import draw_on_map

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

        # Back label
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 1920, 1080)

        # Map
        self.world_map = QLabel(self)
        self.world_map.setGeometry(0, 0, 1536, 864)
        self.pic = QPixmap('assets/map_resize.jpg')
        self.world_map.setPixmap(self.pic)

        # Right side text box
        self.right_box = QLabel(self)
        self.right_box.setGeometry(1536, 0, 357, 800)
        
        # Button
        self.confirm_button = QPushButton('Search', self)
        self.confirm_button.setGeometry(1680, 180, 150, 50)
        self.confirm_button.clicked.connect(self.on_click_update_map)

        # Norad ID text edit
        self.norad_id = QLineEdit(self)
        self.norad_id.setGeometry(1650, 120, 200, 50)

        # Satellite info label
        self.satellite_info_label = QLabel("Satellite Data Here")

        # Example of updating the label with satellite data
        

    def on_click_update_map(self):
        self.iss_id = self.norad_id.text()
        data = satellite_api.get_satellite_position(self.iss_id, observer_lat, observer_long)
        satname = {data}
        satlatitude =
        satlongitude = 
        satellite_str = f"Name: {data['info']['satname']}
        for position in data['positions']:
            satellite_str += f"{position['satlatitude']}, {position['satlongitude']}"

        # Draw satellite on map and update
        new_map_pixmap = draw_on_map(sat_lat, sat_long)
        self.world_map.setPixmap(new_map_pixmap)
