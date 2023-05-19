from azure.storage.blob import BlobServiceClient,ContentSettings

# Configura las credenciales
account_name = "stdevtestaccount"
account_key = "EEHwJ4x1CTKsjapbB/dRV3J8fSK8QsYeH0aGjc7s2aHbMFh6frPpzbkD8i4p88eq1ONantKHnxrT+ASt0rWerw=="
container_name = "test-container"
blob_name = "imageblob"
fileanme = "C:\Users\drubianm\Desktop\perro.jpg"

if __name__=="__main__":


    storage_connection_string='DefaultEndpointsProtocol=https;AccountName=<STORAGE_ACCOUNT_NAME>;AccountKey=<ACCOUNT_KEY>;EndpointSuffix=core.windows.net'
    blob_service_client = BlobServiceClient(conn_str=storage_connection_string)

    container_client = blob_service_client.get_container_client(container=container_name)
    blob_client = container_client.get_blob_client(blob_name)
    if blob_client.exists():
        blob_client.delete_blob()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    try:
        with open(filename, "rb") as data:
             blob.upload(data)
        content_settings =ContentSettings(content_type='image/png')
        logging.debug(f'setting the content type : {content_settings}')
    except Exception as e:
        logging.error(str(e))

