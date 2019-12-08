from .player_ctrl.control import *
# Values:

# Keyboard codes
ESC = 27
# End

# Codes for BGR Colors
BGR_BLUE = (255, 0, 0)
BGR_CYAN = (255, 255, 0)
BGR_RED = (0, 0, 255)
BGR_GREEN = (0, 255, 0)
# End

# Processed Area
    # initial values (for calibration)
X = 100
deltaX = 300
Y = 250
deltaY = 400
    # End

handToFace = -100
extraAreaSize = 5

CaptureSquareToRoi = 15
VD = 25 # valid difference between point and limit to consider gesture
# End

# Limits
edgeLimitSize = 40
# End

# Time
calibrationTime = 8
framesToFace = 20
framesToGesture = 20
# End

# Available control functions
control_dictionary = {
    'GestureType.FIST': fist,
    'GestureType.BIGUP': bup,
    'GestureType.SMALLUP': sup,
    'GestureType.RIGHT': right,
    'GestureType.LEFT': left
}
# End

# Enf of Values
