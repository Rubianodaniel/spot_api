
from typing import BinaryIO
from config.cfg import conecction_string, account_name, container_name
from azure.storage.blob import BlobServiceClient
from responses.response_json import response_json
from generic_functions.decode_image import decode_base64_image

blob_service_client = BlobServiceClient.from_connection_string(conecction_string)


def upload_blob(filename:str, container:str, data:str):
    # try:
        data = decode_base64_image(data)
        blob_client = blob_service_client.get_blob_client(container=container, blob=filename)
        blob_client.upload_blob(data=data)
        return response_json(message="Succes")

    # except Exception as e:
    #     return response_json(message=e.message, status=500)


