import cv2
from PySide6.QtGui import QImage, QPixmap

def draw_on_map(lat, long):
    # Load map
    world_map = cv2.imread('assets/map_resize.jpg')
    height, width, _ = world_map.shape

    # Calc x and y
    x = int((long + 180) * (width / 360))
    y = int((90 - lat) * (height / 180))

    # Draw dot on map
    point_size = 10
    cv2.circle(world_map, (x, y), point_size, (0, 0, 255), -1)

    # Convert the OpenCV image to QPixmap
    world_map_qt = QImage(world_map.data, width, height, world_map.strides[0], QImage.Format_BGR888)
    pixmap = QPixmap.fromImage(world_map_qt)

    return pixmap