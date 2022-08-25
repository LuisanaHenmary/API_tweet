from fastapi import (
    FastAPI,
    status
)

from typing import List

from models.user import User
#uvicorn main:app --reload 
app = FastAPI()

#Default
@app.get(
    path="/"
)
def home():
    return {"Twitter":"Welcome!"}

#Authentication and Users
@app.post(
    path="/auth/signup",
    tags=["Authentication","Users"],
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Registers a new user"
)
def sign_up_user():
    pass

@app.post(
    path="/auth/login",
    tags=["Authentication","Users"],
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a user"
)
def log_in_user():
    pass

#Only Users
@app.get(
    path="/users",
    tags=["Users"],
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Shows all users"
)
def show_all_users():
    pass

@app.get(
    path="/users/{user_id}",
    tags=["Users"],
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a specific user"
)
def show_a_user():
    pass

@app.put(
    path="/users/update/{user_id}",
    tags=["Users"],
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Updates a specific user"
)
def update_a_user():
    pass

@app.delete(
    path="/users/delete/{user_id}",
    tags=["Users"],
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a specific user"
)
def delete_a_user():
    pass

