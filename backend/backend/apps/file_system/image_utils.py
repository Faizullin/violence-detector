def scale_to_min_size(image, min_width, min_height):
    """Returns an image, that isn't smaller than min_width and min_height.
    That means one side is exactly given value and the other is greater.

    This may only makes sense if the image is cut after it is scaled.
    """
    width, height = image.size

    prop_x = float(min_width) / width
    prop_y = float(min_height) / height

    if prop_x > prop_y:
        height = int(prop_x * height)
        image = image.resize((min_width, height))
    else:
        width = int(prop_y * width)
        image = image.resize((width, min_height))

    return image


def scale_to_max_size(image, max_width, max_height):
    """Returns an image, that isn't bigger than max_width and max_height.

    That means one side is exactly given value and the other is smaller. In
    other words the image fits at any rate in the given box max_width x
    max_height.
    """
    width, height = image.size

    prop_width = float(max_width) / width
    prop_height = float(max_height) / height

    if prop_height < prop_width:
        width = int(prop_height * width)
        image = image.resize((width, max_height), )
    else:
        height = int(prop_width * height)
        image = image.resize((max_width, height), )

    return image


def scale_to_width(image, target_width):
    """Returns an image that has the exactly given width and scales height
    proportional.
    """
    width, height = image.size

    prop_width = float(target_width) / width
    new_height = int(prop_width * height)

    image = image.resize((target_width, new_height), )

    return image


def scale_to_height(image, target_height):
    """Returns an image that has the exactly given height and scales width
    proportional.
    """
    width, height = image.size

    prop_height = float(target_height) / height
    new_width = int(prop_height * width)

    image = image.resize((new_width, target_height), )

    return image
