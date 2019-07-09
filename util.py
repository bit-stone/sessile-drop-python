import settings
import numpy as np
import math
import numpy.linalg as npla
from PIL import ImageTk


def image_to_widget(image, widget):
    if(image is not None):
        img_size = image.size
        scale_factor = 1.0
        if(img_size[0] > settings.STANDARD_IMAGE_WIDTH):
            scale_factor = settings.STANDARD_IMAGE_WIDTH / img_size[0]

        new_width = int(img_size[0] * scale_factor)
        new_height = int(img_size[1] * scale_factor)
        image_tk = ImageTk.PhotoImage(
            image=image.resize((new_width, new_height))
        )
        widget.configure(image=image_tk)
        return image_tk
    else:
        print("image to widget: Image was None")
        widget.configure(image="")
# end image_to_widget


def get_scaled_coords(evt, scale_factor):
    mx = int(evt.x * ((1.0) / scale_factor))
    my = int(evt.y * ((1.0) / scale_factor))
    return {"x": mx, "y": my}
# end get_scaled_coords


def get_rescaled_baseline_coords(point, drop_crop, scale_factor):
    dch = drop_crop[3] - drop_crop[1]
    return (
        int((point[0] + drop_crop[0]) * scale_factor),
        int(((dch - point[1]) + drop_crop[1]) * scale_factor)
    )
# end get_rescaled_baseline_coords


def get_rescaled_drop_coords(drop_crop, scale_factor):
    return [
        int(drop_crop[0] * scale_factor),
        int(drop_crop[1] * scale_factor),
        int(drop_crop[2] * scale_factor),
        int(drop_crop[3] * scale_factor)
    ]
# end get_rescaled_drop_coords


def calculate_angle(vec_1, vec_2):
    result = np.dot(vec_1, vec_2) / (
        (npla.norm(vec_1)) * (npla.norm(vec_2))
    )
    result = math.acos(result)

    return result
