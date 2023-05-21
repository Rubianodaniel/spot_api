import re
import pytz
from fastapi import HTTPException, status
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from generic_functions.replacetext import extract_base64_image
from images_prueba import imagen1



class CemerasDataSerializer(BaseModel):
    id: Optional[str]
    date: Optional[datetime]
    image_base64: str
    camera_id: str

    class Config:
        fields = {
            'id': Field(..., alias='_id'),
            
        }
        orm_mode = True
        schema_extra = {
            "example": {
                "image_base64":imagen1,
                "camera_id": "123456"
            }
        }
    


    @validator('image_base64')
    def validate_image_base64(cls, image_base64):
        if not image_base64:
            raise HTTPException(status_code=400, detail="The image_base64 field cannot be empty.")
        
        pattern = r'^data:image/jpeg;base64,(.*)$'
        image_base64 = extract_base64_image(image_base64, pattern=pattern)
        if not image_base64: 
            raise HTTPException(status_code=422, detail="The format of image_base64 is not correct" )
        return image_base64
    
    
    @validator('camera_id')
    def validate_camera_id(cls, camera_id):
        if not camera_id:
            raise HTTPException(status_code=400, detail="The camera_id field cannot be empty.")
        return camera_id
    


