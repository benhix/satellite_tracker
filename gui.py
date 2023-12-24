import geocoder
from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
import satellite_api

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

        layout = QVBoxLayout()

        # Satellite info label
        self.satellite_info_label = QLabel("Satellite Data Here")
        layout.addWidget(self.satellite_info_label)

        self.central_widget.setLayout(layout)

        # Example of updating the label with satellite data
        data = satellite_api.get_satellite_position(iss_id, observer_lat, observer_long)
        self.satellite_info_label.setText(str(data))
