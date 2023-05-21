import base64
import io
from PIL import Image

filepath = "C:/Users/drubianm/Pictures/prueba"

async def decode_base64_image(image_base64, filename):
    """
    Decodes a base64-encoded image and saves it as a file.

    Args:
        image_base64 (str): Base64-encoded image data.
        filename (str): Name of the file to be saved.

    Returns:
        bytes: Decoded image data.

    Raises:
        None.
    """
 
    image = base64.b64decode(image_base64)
 
    with open(f"{filepath}/{filename}", "wb") as file:
        file.write(image)
    return image