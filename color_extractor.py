import numpy as np # To process RGB values
from PIL import Image # To Load Image
from collections import Counter


def get_top_colors(image_path, top10=10):
    # Opens the image and converts it to RGB. We do this in case of Greyscale or transparency
    img = Image.open(image_path).convert("RGB") 
    # Creates a numpty array (height, width, 3)
    img_array = np.array(img)
    # Reshape image to a list of pixels. Need this to count flat lists, instead of 3D arrays
    pixels = img_array.reshape(-1, 3)
    # Converts our reshaped array into hex codes for pixels. Much easier to use later. The formatting 02x converts numbers to HEX, but ensuring two digits
    hex_pixels = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in pixels]
    # Count the times each color appears
    color_count = Counter(hex_pixels)
    # Sort the top number of colors
    common_colors = color_count.most_common(top10)

    # To convert to a dictionary with percentages
    total_pixels = len(hex_pixels)
    color_dict = {color: round((count / total_pixels) * 100, 2) for color, count in common_colors}

    return color_dict