from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from azure_blod_storage.upload_azure import upload_blob
from models.camerasdatamodel import CamerasDataModel
from serialzers.camerasdataserializer import CemerasDataSerializer
from sqlalchemy.exc import SQLAlchemyError
from config.db import session


router = APIRouter(prefix="/cameras",
                   tags=["cameras"],
                   responses={status.HTTP_404_NOT_FOUND:{"message":"Not Found"}}
                )


def create_data_in_db(data, db):
 
    try:
        
        new_data = CamerasDataModel(image_base64 = data.image_base64,
                                    camera_id = data.camera_id
                                    )
        
        db.add(new_data)
        db.flush()
        db.commit()
        db.refresh(new_data)
        return new_data
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    finally:
        db.close()



@router.get("/", status_code=status.HTTP_200_OK)
async def list_data_camera():
    db = session()
    return db.query(CamerasDataModel).all()
    

    


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(data:CemerasDataSerializer):
    db = session()
    try:
        new_data = create_data_in_db(data, db)
        return {"message": "la data se ha creado correctamente", "data": new_data}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=str(e))
    

@router.post("/upload")
async def upload(container:str = Form(...), file:UploadFile = File(...)):
    data = await file.read()
    filename = file.filename
    return upload_blob(filename, container, data)
