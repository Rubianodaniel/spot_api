
from fastapi import HTTPException, status
from models.camerasdatamodel import CamerasDataModel
from sqlalchemy.exc import SQLAlchemyError




async def create_data_in_db(data, db):
    """
    Creates a new entry in the database with the provided data.

    Args:
        data: The data to be saved in the database.
        db: The database session.

    Returns:
        CamerasDataModel: The newly created data entry.

    Raises:
        HTTPException: If there is an error during the database operation.
    """
    try:
        if data.date is not None:
            new_data = CamerasDataModel(
                                    date = data.date,
                                    image_base64 = data.image_base64,
                                    camera_id = data.camera_id
                                    )
        else:
            new_data = CamerasDataModel(image_base64 = data.image_base64,
                        camera_id = data.camera_id
                        )

        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        return new_data
       
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        db.close()
