from fastapi import HTTPException
from fastapi.responses import JSONResponse
from config.cfg import connection_string
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError, ClientAuthenticationError, AzureError


from generic_functions.decode_image import decode_base64_image

async def conection_azure(connection_string):

    """
    connection to Azure Blob Storage using the provided connection string.

    Args:
        connection_string (str): Azure Blob Storage connection string.

    Returns:
        blob_service_client (BlobServiceClient): Azure Blob service client.

    Raises:
        HTTPException: Raised if there is a client authentication error.
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        return blob_service_client
    
    except AttributeError as e:
        raise HTTPException(status_code=401, detail="Client authentication error.")



async def upload_blob(filename:str, container:str, image_base64:str):
    
    """
    Uploads a image file to Azure Blob Storage.

    Args:
        filename (str): Name of the image file.
        container (str): Name of the container in Azure Blob Storage.
        image_base64 (str): Base64 encoded image.

    Returns:
        JSONResponse: JSON response with the success message and status code 201.

    Raises:
        HTTPException: Raised if the file already exists in the container,
                       if the file or container does not exist, or if there is an Azure error.
    """
        
    try:
        data = await decode_base64_image(image_base64, filename)
        blob_service_client = await conection_azure(connection_string=connection_string)
        blob_client = blob_service_client.get_blob_client(container=container, blob=filename)
        blob_client.upload_blob(data=data)
        return JSONResponse(content={"message": "Image successfully uploaded to Azure storage"}, status_code=201)
    

    except ResourceExistsError:
        raise HTTPException(status_code=409, detail="The file already exists in the container.")
    
    except ResourceNotFoundError:
        raise HTTPException(status_code=404, detail="The file or container does not exist.")



        

