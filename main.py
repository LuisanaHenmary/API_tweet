from fastapi import (
    FastAPI,
    status
)

from typing import List

from models.tweet import Tweet
from models.user import User
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
def sign_up_user():
    pass

#user login
@app.post(
    path="/auth/login",
    tags=["Authentication","Users"],
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a user"
)
def log_in_user():
    pass

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
    pass

#show a specific user
@app.get(
    path="/users/{user_id}",
    tags=["Users"],
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a specific user"
)
def show_a_user():
    pass

#updates a specific user
@app.put(
    path="/users/update/{user_id}",
    tags=["Users"],
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Updates a specific user"
)
def update_a_user():
    pass

#delete a specific user
@app.delete(
    path="/users/delete/{user_id}",
    tags=["Users"],
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a specific user"
)
def delete_a_user():
    pass

###TWEETS###

#shows all tweets
@app.get(
    path="/tweets",
    tags=["Tweets"],
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Shows all tweets"

)
def show_all_twets():
    return {"estado":"en construccion"}

#post a new tweet
@app.post(
    path="/tweet",
    tags=["Tweets"],
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a new tweet"
)
def post_new_tweet():
    pass

#show a specific tweet
@app.get(
    path="/tweet/{tweet_id}",
    tags=["Tweets"],
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    response_model=Tweet
)
def show_a_tweet():
    pass

#update a specific tweet
@app.put(
    path="/tweet/update/{tweet_id}",
    tags=["Tweets"],
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    response_model=Tweet
)
def update_a_tweet():
    pass

#delete a specific tweet
@app.delete(
    path="/tweet/delete/{tweet_id}",
    tags=["Tweets"],
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    response_model=Tweet
)
def delete_a_tweet():
    pass

