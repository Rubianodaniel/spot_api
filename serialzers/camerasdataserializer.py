import re
from fastapi import HTTPException
from pydantic import BaseModel, Field, validator
from typing import Optional



class CemerasDataSerializer(BaseModel):
    id: Optional[str]
    date: Optional[str]
    image_base64: str
    camera_id: str

    class Config:
        fields = {
            'id': Field(..., alias='_id'),
            
        }
        orm_mode = True
        schema_extra = {
            "example": {
                "image_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAAXNSR0IArs4c6QAAIABJREFUOBGVk39vUdW5/++7cubtloIwBRIIQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADA9QLZpfUqo1P/7Saq1DfJWY+mKJOXR8qUhZ1EVSqyNzHJPucVfdO9/Npu3e5w6eP1rjn7X25PtmPTs3/muTd9Ft3LW58W1rjvtbJ9erL65D1rKZ1D5OfqkZ0vzvnUt3PY6KzK3OfLzRm8JldllrrDyqqe0p5b3nlLK+d/qdva+yvneTyztmxyXmmxRvUeqVYsSOu9HkOnmvS8iW8f2ftjW2Nlz5x1rc/c9KJdjzax4NvP1/Zn95JXu7q4cO/Nnrh9rhd2b3Xj4kLl/92OjX7alnWbhH6XN3dL6j1rLaR3veoXt1qqsKb45t33b90vHbW3POeUn2esRw8XRpyaIkk3dz/7Fnlz6VLfr8by8/3BfZfY03VL1e2duWz6Yfnfu0/fA96xzc8mNztXz+s+rHaG8/k+/u8iXtNTlvfn9mXz48H1+zm88p24W1ZXj2tq5PJj2eS6P1vW83bTzX+vp+tVu2L9r/e/pR8fv2VU/R3r59un8Xc3J4pYfjtPnfY9TVHX2X3xYds8rrb3/8bQ+td3mzq6XfmmnH7V6l7m4f2x9g+F3J48Q/R5Q6t1L1T3ZXmLjuVJ9bmUyazDc/9e+w",
                "camera_id": "123456"
            }
        }


    @validator('image_base64')
    def validate_image_base64(cls, image_base64):
        if not image_base64:
            raise HTTPException(status_code=400, detail="The image_base64 field cannot be empty.")
        
        pattern = r'^data:image/[a-zA-Z]+;base64,'
        if not re.match(pattern, image_base64):
            raise HTTPException(status_code=422, detail="The format of image_base64 is wrong" )
        return image_base64
    
    
    @validator('camera_id')
    def validate_camera_id(cls, camera_id):
        if not camera_id:
            raise HTTPException(status_code=400, detail="The camera_id field cannot be empty.")
        return camera_id