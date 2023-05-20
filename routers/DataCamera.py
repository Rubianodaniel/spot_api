from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from config.db import get_session
from azure_blod_storage.upload_azure import upload_blob
from models.camerasdatamodel import CamerasDataModel
from serialzers.camerasdataserializer import CemerasDataSerializer
from responses.response_json import response_json




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
async def list_data_camera(db: Session = Depends(get_session)):
    lst_data = db.query(CamerasDataModel).all()        
    db.close()
    return lst_data


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_data(data:CemerasDataSerializer, db: Session = Depends(get_session)):
    try:
        new_data = create_data_in_db(data, db)

        return {"message": "la data se ha creado correctamente", "data": new_data}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=str(e))

    
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_data(id:str, db: Session = Depends(get_session)):
    try:
        db.query(CamerasDataModel).filter(CamerasDataModel.id == id).delete()
        db.commit() 
        return 
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    finally:
        db.close()
    

@router.post("/upload/{id}")
async def upload_data_by_id(id:str, db: Session = Depends(get_session)):

    objeto = db.query(CamerasDataModel).filter(CamerasDataModel.id == id).first()
    camera_id = objeto.camera_id
    filename = f"{camera_id}-{str(objeto.date)}"
    image = objeto.image_base64 
    db.close()
    return upload_blob(filename=filename, container="test-container", image_base64=image)



@router.post("/upload/{id}")
async def upload_data_by_batch(id:str, db: Session = Depends(get_session)):

    objeto = db.query(CamerasDataModel).filter(CamerasDataModel.id == id).first()
    camera_id = objeto.camera_id
    filename = f"{camera_id}-{str(objeto.date)}"
    image = objeto.image_base64 
    db.close()
    return upload_blob(filename=filename, container="test-container", image_base64=image)


