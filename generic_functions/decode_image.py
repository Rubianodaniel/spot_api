import base64
import io
from PIL import Image

def decode_base64_image(image_base64):
 
    image_data = base64.b64decode(image_base64)
    image = io.BytesIO(image_data)
    return image