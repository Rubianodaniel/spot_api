import base64
import io
from PIL import Image



async def decode_base64_image(image_base64):
    """
    Decodes a base64-encoded image and saves it as a file.

    Args:
        image_base64 (str): Base64-encoded image data.

    Returns:
        bytes: Decoded image data.

    Raises:
        None.
    """
 
    image = base64.b64decode(image_base64)
 

    return image