
from azure.storage.blob import BlobServiceClient



def conexion_azure(connection_string):
    # Crear una conexión al servicio de almacenamiento de Blob de Azure
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    return blob_service_client