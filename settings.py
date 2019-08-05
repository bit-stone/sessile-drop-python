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
IMAGE_INPUT_FRAME_DELAY = 16

# standard image width
STANDARD_IMAGE_WIDTH = 1280


# #### Default settings for edge detection
# #
# Threshold for bw_threshold_linear method
# this is the default value for the slider on edge detection page
BW_DEFAULT_THRESHOLD = 60

# Threshold for edge on black/white image
BW_LINEAR_THRESHOLD = 70

# top/bottom threshold for sobel_canny
SOBEL_DEFAULT_TOP = 250
SOBEL_DEFAULT_BOTTOM = 50

# values for needle detection.
# these should be different from drop values
# as the needle usually is easily detected
SOBEL_NEEDLE_TOP = 230
SOBEL_NEEDLE_BOTTOM = 100

# ### Fitting ######################

# ## Fitting Tangent 1
# order of polynom fitted to left/right points
FT1_POLYNOM_ORDER = 3
# ratio of height to width over which coords should
# be flipped for better fitting performance
FT1_FLIP_THRESHOLD = (3.0/8.0)
# number of points for fitting
FT1_POINT_COUNT = 50

# ## Fitting Tangent 2
# order of polynom fitted to left/right points
FT2_POLYNOM_ORDER = 3
# number of points for fitting
FT2_POINT_COUNT = 50
# offset for binary search
FT2_BIN_SEARCH_OFFSET = 10
# max number of binary steps
FT2_BIN_SEARCH_MAX_COUNT = 50
# desired binary search distance
FT2_BIN_SEARCH_DELTA_X = 0.0001


# ### Fluid-Data Settings #################
# which index refers to which value
FLUID_IDX_IFT = 1
FLUID_IDX_DISPERSE = 2
FLUID_IDX_POLAR = 3
FLUID_IDX_DENSITY = 4
FLUID_IDX_VISCOSITY = 5
FLUID_IDX_TEMPERATURE = 6

# ### Save-Load-Names #######################
# name of result files
TEST_RESULT_FILE_NAME = "test_result.csv"
TEST_SERIES_RESULT_FILE_NAME = "test_series_result.csv"
TEST_SERIES_FILE_COL_COUNT = 11

SAVE_IDX_INDEX = 0
SAVE_IDX_LABEL = 1
SAVE_IDX_FLUID = 2
SAVE_IDX_FIT_METHOD = 3
SAVE_IDX_EDGE_METHOD = 4
SAVE_IDX_EDGE_TOP_BOTTOM = 5
SAVE_IDX_DROP_CROP = 6
SAVE_IDX_NEEDLE_CROP = 7
SAVE_IDX_BASELINE_FIRST_SECOND = 8
SAVE_IDX_ANGLE = 9
SAVE_IDX_DEVIATION = 10

SAVE_COL_LABELS = {
    SAVE_IDX_INDEX: "index",
    SAVE_IDX_LABEL: "label",
    SAVE_IDX_FLUID: "fluid",
    SAVE_IDX_FIT_METHOD: "fit_method",
    SAVE_IDX_EDGE_METHOD: "edge_method",
    SAVE_IDX_EDGE_TOP_BOTTOM: "edge_top_bottom",
    SAVE_IDX_DROP_CROP: "drop_crop",
    SAVE_IDX_NEEDLE_CROP: "needle_crop",
    SAVE_IDX_BASELINE_FIRST_SECOND: "baseline_first_second",
    SAVE_IDX_ANGLE: "angle",
    SAVE_IDX_DEVIATION: "deviation"
}
