from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from config.db import session, Base, engine
from models.users import UsersModel, PasswordModel
from serialzers.userserializer import UserModelSerializer

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
ALGORITHM = "HS256"
ACCES_TOKEN_DURATION = 30
SECRET_KEY = "MYSECRETKEY"
crypt = CryptContext(schemes=["bcrypt"])


router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={404:{"message":"Not found"}}
                )


class User(BaseModel):
    username:str
    name:str
    lastname:str
    age:str
    disable:bool

class UserDB(User):
    password:str

users_db = {
    "daniel":{
            "username": "daniel",
            "name":"danielrubiano",
            "lastname":"rubiano",
            "age":"27",
            "disable":False,
            "password" : "$2a$12$WlfLaenfDGN3iPFtoKcNSOJd.dSmaG4h.4XSVGTpC3Ol1GPriGG6G"
    },
    "daniel2":{
            "username": "daniel2",
            "name":"danielrubiano2",
            "lastname":"rubiano2",
            "age":"27",
            "disable":True,
            "password" : "$2a$12$GIiqGXo7AANwv3ukTpw2k.pzssGf8ZvMaYJiAFC62vjiRsahbU8K."
    }
}

def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])
    

def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])


async def auth_user(token:str = Depends(oauth2)):

    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="credenciales de autenticacion invalidas",
                    headers={"WWW-autenticate":"Bearer"}
                    )
    try:
        username = jwt.decode(token, SECRET_KEY ,algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception


    except JWTError:
        raise exception
    
    return search_user(username=username)
    


async def current_user(user:str = Depends(auth_user)):
  
    if user.disable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario no autorizado",
                            headers={"WWW-autenticate":"Bearer"}
                            )
    return user



@router.post("/login")
async def login(form:OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(username = form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
  

    acces_token = {"sub" : user.username,
                   "exp" : datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_DURATION)                  
                }


    return {"access_token": jwt.encode(acces_token, SECRET_KEY, algorithm=ALGORITHM) , "token_type":"bearer"}
    


@router.get("/")
async def list_users():
    db = session()

    lst_users = db.query(UsersModel).all()
    return lst_users





@router.get("/me")
async def get_user(user:User = Depends(current_user)):
    return user



def create_user_in_database(user):
    db = session()
    try:

        user_exists = db.query(UsersModel).filter(UsersModel.username == user.username).exists()
        if db.query(user_exists).scalar():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                    detail="User already exist",
                )

        password = PasswordModel(password=user.password)
        db.add(password)
        new_user = UsersModel(username=user.username, name=user.name, lastname=user.lastname,
                              age=user.age, disable=user.disable, password_id=password.id)
        db.add(new_user)
        db.flush()
        db.commit()
        return new_user
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    finally:
        db.close()



@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user:UserModelSerializer):
    create_user_in_database(user)


    return {"message": "Usuario creado exitosamente", "user": user.dict(exclude={'password'})}