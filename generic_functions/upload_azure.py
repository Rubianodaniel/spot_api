import io
from config.cfg import conecction_string, account_name, container_name
from generic_functions.decode_image import decode_base64_image
from config.conexion_azure import conexion_azure


def upload_images_to_azure(image_base64):
    image = decode_base64_image(image_base64=image_base64)
    
    # Conexión a Azure Storage
    blob_service_client = conexion_azure(connection_string=conecction_string)
    
    # Nombre del archivo en Azure Storage (puedes usar un nombre único)
    blob_name = "image.jpg"
    
    # Obtener el contenedor de almacenamiento en Azure
    container_client = blob_service_client.get_container_client(container=container_name)
    
    # Convertir la imagen en formato BytesIO
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="JPEG")
    image_bytes.seek(0)
    
    # Subir la imagen a Azure Storage
    container_client.upload_blob(name=blob_name, data=image_bytes)
    
    # Devolver la URL de acceso a la imagen en Azure Storage
    image_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}"
    
    return image_url
