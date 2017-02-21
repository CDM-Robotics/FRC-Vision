
# TODO - set to reflector width in inches
KNOWN_WIDTH = 0

# TODO (One time calc for focalLength)
# formula: (pixel_width * known_distance)/known_width
FOCAL_LENGTH = 0

# width in inches, computer focal length, and width in pixels
def camera_distance(width=0, focal_length=0, pixel_width=0):
    return (width * focal_length)/pixel_width

