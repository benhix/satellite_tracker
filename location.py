import cv2

def draw_on_map(lat, long):
    # Load map
    world_map = cv2.imread('assets/map_resize.jpg')
    height, width = world_map.shape

    # Calc x and y
    x = int((long + 180) * (width / 360))
    y = int((90 - lat) * (height / 180))

    # Draw dot on map
    point_size = 50
    cv2.circle(world_map, (x, y), point_size, (0, 0, 255), -1)

    return world_map