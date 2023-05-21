
from fastapi import APIRouter, Depends, HTTPException, status
import asyncio

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from generic_functions.create_data_db import create_data_in_db
from generic_functions.replacetext import clean_filename

from config.db import get_session
from config.cfg import container_name

from azure_blod_storage.upload_azure import upload_blob
from models.camerasdatamodel import CamerasDataModel
from serialzers.list_data_camera_serializer import ListCamerasDataSerializer
from serialzers.camerasdataserializer import CemerasDataSerializer



router = APIRouter(prefix="/cameras",
                   tags=["cameras"],
                   responses={status.HTTP_404_NOT_FOUND:{"message":"Not Found"}}
                )


@router.get("/", status_code=status.HTTP_200_OK)
async def list_data_camera(db: Session = Depends(get_session)):
    """
    Retrieves a list of camera data from the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        List[CamerasDataModel]: List of camera data.

    Raises:
        None.
    """
    lst_data = db.query(CamerasDataModel).all()        
    db.close()
    return lst_data


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_data(data:CemerasDataSerializer, db: Session = Depends(get_session)):
    """
    Creates new data in the database and uploads the image to Azure Blob Storage.

    Args:
        data (CemerasDataSerializer): Data of the camera image.
        db (Session): Database session dependency.

    Returns:
        dict: Dictionary containing the success message and the created data.

    Raises:
        HTTPException: Raised if there is an HTTP exception during the process.
    """
    try:
        new_data = await create_data_in_db(data, db)
        camera_id = new_data.camera_id
        filename = f"{camera_id}{str(new_data.date)}.jpg"
        filename = clean_filename(filename)
        image = new_data.image_base64 
        response = await upload_blob(filename=filename, container=container_name, image_base64=image)
        context = {
            "message":response,
            "data": new_data
        }
        return context
    
    except HTTPException as e:
        raise e
    
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_data(id:str, db: Session = Depends(get_session)):
    """
    Deletes data from the database.

    Args:
        id (str): ID of the data to be deleted.
        db (Session): Database session dependency.

    Returns:
        None.

    Raises:
        HTTPException: Raised if the data to be deleted is not found or if there is an internal server error.
    """
    try:
        result = db.query(CamerasDataModel).filter(CamerasDataModel.id == id).delete()
        if result == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    



@router.post("/upload_list/", status_code=status.HTTP_201_CREATED)
async def upload_data_by_batch(list_data: ListCamerasDataSerializer, db: Session = Depends(get_session)):
    """
    Uploads a batch of data to the database and Azure Blob Storage.

    Args:
        list_data (ListCamerasDataSerializer): List of camera data to be uploaded.
        db (Session): Database session dependency.

    Returns:
        dict: Dictionary containing the success message and the uploaded data.

    Raises:
        SQLAlchemyError: Raised if there is a SQLAlchemy error during the process.
        HTTPException: Raised if there is an HTTP exception during the process.
    """
    try:

        if len(list_data.data) > 100:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No more than 100 photos may be uploaded in a single request.")
        
        lst_new_data = []
        
        for element in list_data:
            for data in element[1]:
                task = create_data_in_db(data, db)
                lst_new_data.append(task)

        results = await asyncio.gather(*lst_new_data)

        lst_ids = []    
        upload_tasks = []
            
        for element in results:
            lst_ids.append(element.id)
            camera_id = element.camera_id
            filename = f"{camera_id}{str(element.date)}.jpg"
            filename = clean_filename(filename)
            image = element.image_base64 
            task = upload_blob(filename=filename, container=container_name, image_base64=image)
            upload_tasks.append(task)
        
        await asyncio.gather(*upload_tasks)

        query = db.query(CamerasDataModel).filter(CamerasDataModel.id.in_(lst_ids)).all()

        return {"message": "La lista de datos se ha creado correctamente", "data": query}

    except SQLAlchemyError as e:
        db.rollback()
        raise e
    
    except HTTPException as e:
        raise e

    









