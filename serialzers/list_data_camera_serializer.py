from typing import List
from pydantic import BaseModel
from serialzers.camerasdataserializer import CemerasDataSerializer
from images_prueba import imagen1, imagen2, imagen3

class ListCamerasDataSerializer(BaseModel):
    data: List[CemerasDataSerializer]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "data": [
                    {
                        "image_base64":imagen1,
                        "camera_id": "123456"
                    },
                    {
                        "image_base64": imagen2,         
                        "camera_id": "123456"
                    },
                    {
                        "image_base64": imagen3,                  
                        "camera_id": "1234567"
                    }
              
                ]
            }
        }