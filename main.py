import json
from io import open

from typing import List

from fastapi import (
    FastAPI,
    status,
    Body
)

from models.tweet import Tweet
from models.user import (
    User,
    UserRegister
)
#uvicorn main:app --reload 
app = FastAPI()
###DEFAULT###

#home
@app.get(
    path="/"
)
def home():
    return {"Welcome to view api documentation":"http://127.0.0.1:8000/redoc"}

###AUTHENTICATION AND USERS###

#user register
@app.post(
    path="/auth/signup",
    tags=["Authentication","Users"],
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Registers a new user"
)
def sign_up_user(user: UserRegister = Body(...)):
    """
        SignUp a user

        This path operation register a user in the app

        Parameters:
            - Request body parameters
                - user: UserRegister

        Return a json with the basic user information:
            - user_id: UUID
            - email: EmailStr
            - user_name: str
            - first_name: str
            - last_name: str
            - birth_date: date
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        f.close()
        return user


###ONLY USERS###

#show all users
@app.get(
    path="/users",
    tags=["Users"],
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Shows all users"
)
def show_all_users():
    """
        Show all users

        This path operation shows all users in the app

        Parameters:
            - 

        Return a json list with all users in the app, with the following keys
            - user_id: UUID
            - email: EmailStr
            - user_name: str
            - first_name: str
            - last_name: str
            - birth_date: date
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results
