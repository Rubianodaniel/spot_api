from fastapi import APIRouter


router = APIRouter(prefix="/datacamera",
                   tags=["datacamera"],
                   responses={404:{"message":"Not found"}}
                )


@router.get("/")
async def create_message():
    return "hola"


 
@router.get("/{id}")
async def create_message(id:int):
    return str(id)