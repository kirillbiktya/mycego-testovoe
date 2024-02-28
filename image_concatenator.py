from typing import List
from PIL import Image
import math

IMAGE_PADDING_PX = 50
OUTER_PADDINGS_COUNT = 3
CHILD_IMAGE_SIZE = (800, 800)


def concat(images: List[Image.Image]):
    img_count = len(images)
    if img_count == 0:
        raise Exception("Cannot operate without images!")

    if math.sqrt(img_count) - math.floor(math.sqrt(img_count)):
        rows = math.floor(math.sqrt(img_count))
        cols = rows + 1
    else:
        rows = cols = math.sqrt(img_count)

    full_height = IMAGE_PADDING_PX * OUTER_PADDINGS_COUNT * 2 + rows * CHILD_IMAGE_SIZE[1] + (rows - 1) * IMAGE_PADDING_PX
    full_width = IMAGE_PADDING_PX * OUTER_PADDINGS_COUNT * 2 + cols * CHILD_IMAGE_SIZE[0] + (cols - 1) * IMAGE_PADDING_PX

    full_image = Image.new('RGBA', (full_width, full_height), 'white')

    img_in_row = 0
    pos = [IMAGE_PADDING_PX * OUTER_PADDINGS_COUNT, IMAGE_PADDING_PX * OUTER_PADDINGS_COUNT]  # w,h
    for image in images:
        image_resized = image.resize(CHILD_IMAGE_SIZE)
        if img_in_row < cols:
            full_image.paste(image_resized, (pos[0], pos[1], pos[0] + CHILD_IMAGE_SIZE[0], pos[1] + CHILD_IMAGE_SIZE[1]))
            img_in_row += 1
            pos[0] += CHILD_IMAGE_SIZE[0] + IMAGE_PADDING_PX
        else:
            img_in_row = 0
            pos[0] = IMAGE_PADDING_PX * OUTER_PADDINGS_COUNT
            pos[1] += IMAGE_PADDING_PX + CHILD_IMAGE_SIZE[1]

    return full_image


