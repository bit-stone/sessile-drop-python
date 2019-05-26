# #### Settings for image input
# #
# desired frame size of camera
IMAGE_INPUT_FRAME_WIDTH = 1280
IMAGE_INPUT_FRAME_HEIGHT = 720

# duration of one frame in image input preview
# measured in milliseconds
# should be big enough to not cause lags
# 20 fps => 1000 / 20 = 50 ms
# 30 fps => 1000 / 30 = 33 ms
# 50 fps => 1000 / 50 = 20 ms
# 60 fps => 1000 / 60 = 16 ms
IMAGE_INPUT_FRAME_DELAY = 50


# #### Default settings for edge detection
# #
# Threshold for bw_threshold_linear method
BW_DEFAULT_THRESHOLD = 60

# Threshold for edge on black/white image
BW_LINEAR_THRESHOLD = 70

# top/bottom threshold for sobel_canny
SOBEL_DEFAULT_TOP = 250
SOBEL_DEFAULT_BOTTOM = 50



# ### Fitting ######################
# ## Fitting Tangent 1
FT1_POLYNOM_ORDER = 3
