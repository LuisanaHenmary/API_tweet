#python native
import re
from typing import List
from uuid import UUID
from datetime import datetime

#fastapi
from fastapi import (
    FastAPI,
    status,
    HTTPException,
    Path,
    Body
)

#models directory
from models.tweet import (
    Tweet,
    UpdateTweet
)

from models.user import (
    User,
    UserRegister
)

#utils directory
from utils.funtions import (
    run_query,
    user_dict,
    tweet_dict,
    get_user_dict,
    get_tweet_dict
)

#uvicorn main:app --reload 
app = FastAPI()

###DEFAULT###

#home
@app.get(
    path="/",
    summary="A default link"
)
def home():

    """
        Home

        This is the default path operation

        Parameters:\n
            -

        Return a json with a link for the documentation of the api:\n
            - Link doc: str

    """

    return {"Link doc":"http://127.0.0.1:8000/redoc"}

### USERS ###

#user register
@app.post(
    path="/auth/signup",
    tags=["Users"],
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Registers a new user"
)
def sign_up_user(user: UserRegister = Body(...)):

    """
        SignUp a user

        This path operation register a user in the app

        Parameters:\n
            - Request body parameters
                - user: UserRegister

        Return a json with the basic user information:\n
            - user_id: UUID
            - email: EmailStr
            - user_name: str
            - first_name: str
            - last_name: str
            - birth_date: date
    """

    query = "INSERT INTO user VALUES(?,?,?,?,?,?,?)"
    
    parameters = (
        str(user.user_id),
        user.email,
        user.user_name,
        user.first_name,
        user.last_name,
        user.birth_date,
        user.password
    )

    try:
        run_query(query, parameters)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This user alredy exist"
        )
    
    return user

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

        Parameters:\n
            - 

        Return a json list with all users in the app, with the following keys\n
            - user_id: UUID
            - email: EmailStr
            - user_name: str
            - first_name: str
            - last_name: str
            - birth_date: date
    """

    query = "SELECT * FROM user"

    list_users = []

    resp = run_query(query)

    for ele in resp:
        list_users.append(user_dict(ele))

    return list_users

#show a specific user
@app.get(
    path="/users/{user_id}",
    tags=["Users"],
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a specific user"
)
def show_a_user( 
    user_id: UUID = Path(
        ...,
        title="User ID",
        description="It is the ID of one of many users"
    )):

    """
        Show a user

        This path operation shows only one user

        Parameters:\n
            - user_id: UUID

        Return a json with the user info in the app, with the following keys\n
            - user_id: UUID
            - email: EmailStr
            - user_name: str
            - first_name: str
            - last_name: str
            - birth_date: date
    """

    return get_user_dict(user_id)

#updates a specific user
@app.put(
    path="/users/update/{user_id}",
    tags=["Users"],
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Updates a specific user"
)
def update_a_user(
    user_id: UUID = Path(
        ...,
        title="User ID",
        description="It is the ID of one of many users"
    ),
    user: UserRegister = Body(...)):

    """
        Show a user

        This path operation update only one user

        Parameters:\n
            - user_id: UUID
            - Request body parameters
                - user: UserRegister

        Return a json with the user info in the app, with the following keys\n
            - user_id: UUID
            - email: EmailStr
            - user_name: str
            - first_name: str
            - last_name: str
            - birth_date: date
    """

    get_user_dict(user_id)

    query = f"""UPDATE user SET 
    user_name='{user.user_name}',
    password='{user.password}'
    WHERE user_id='{user_id}' """

    run_query(query)

    query = f"""UPDATE tweet SET 
    user_name='{user.user_name}',
    updated_at='{datetime.now()}'
    WHERE user_id='{user_id}' """

    run_query(query)

    return user

    #delete a specific user
@app.delete(
    path="/users/delete/{user_id}",
    tags=["Users"],
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a specific user"
)
def delete_a_user(
    user_id: UUID = Path(
        ...,
        title="User ID",
        description="It is the ID of one of many users"
    )):

    """
        Show a user

        This path operation delete only one user

        Parameters:\n
            - user_id: UUID

        Return a json with the user info in the app, with the following keys\n
            - user_id: UUID
            - email: EmailStr
            - user_name: str
            - first_name: str
            - last_name: str
            - birth_date: date
    """

    query = f"DELETE FROM tweet WHERE user_id='{user_id}'"
    run_query(query)

    dict_resp = get_user_dict(user_id)

    query = f"DELETE FROM user WHERE user_id='{user_id}'"
    run_query(query)

    return dict_resp

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

    """
        Show all tweets 

        This path operation shows all tweet in the app

        Parameters:\n
            - 

        Return a json list with all tweets in the app, with the following keys\n
            - tweet_id: UUID
            - content: str
            - created_at: datetime
            - updated_at: datetime
            - by: User
    """

    query = "SELECT * FROM tweet"

    list_tweets = []

    resp = run_query(query)

    for ele in resp:
        list_tweets.append(tweet_dict(ele))

    return list_tweets

#show user's tweets
@app.get(
    path="/tweets/{user_id}",
    tags=["Tweets"],
    status_code=status.HTTP_200_OK,
    summary="Show a user's tweets",
    response_model=List[Tweet]
)
def show_a_user_tweet(user_id: UUID = Path(
    ...,
    title="User ID",
    description="It is the ID of one of many users"
)):

    """
        Show all tweets of a single user

        This path operation shows all tweets from a specific user

        Parameters:\n
            - user_id: UUID

        Return a json list with all the tweets of a single user in the app, with the following keys\n
            - tweet_id: UUID
            - content: str
            - created_at: datetime
            - updated_at: datetime
            - by: User
    """

    query = f"SELECT * FROM tweet WHERE user_id='{user_id}'"

    list_tweets = []

    resp = run_query(query)
    for ele in resp:
        list_tweets.append(tweet_dict(ele))

    return list_tweets

#show a specific tweet
@app.get(
    path="/tweet/{tweet_id}",
    tags=["Tweets"],
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    response_model=Tweet
)
def show_a_tweet(tweet_id: UUID = Path(
    ...
)):

    """
        Show a specific tweet

        This path operation shows only one tweet

        Parameters:\n
            - tweet_id: UUID

        Return a json list with the tweet info in the app, with the following keys\n
            - tweet_id: UUID
            - content: str
            - created_at: datetime
            - updated_at: datetime
            - by: User
    """

    return get_tweet_dict(tweet_id)

#post a new tweet
@app.post(
    path="/tweet",
    tags=["Tweets"],
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a new tweet"
)
def post_new_tweet(tweet: Tweet = Body(...)):

    """
        Post a tweet

        This path operation post a tweet in the app

        Parameters:\n
            - Request body parameters
                - tweet: Tweet

        Return a json list with the tweet info in the app, with the following keys\n
            - tweet_id: UUID
            - content: str
            - created_at: datetime
            - updated_at: datetime
            - by: User
    """

    query = f"SELECT * FROM user WHERE user_id='{tweet.by.user_id}'"
    resp = run_query(query)

    if len(resp.fetchall()) == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This user does not exist"
        )

    query = "INSERT INTO tweet VALUES(?,?,?,?,?,?)"

    tweet.created_at = datetime.now()
    tweet.updated_at = datetime.now()

    parameters = (
        str(tweet.tweet_id),
        str(tweet.by.user_id),
        tweet.by.user_name,
        tweet.content,
        str(tweet.created_at),
        str(tweet.updated_at)
    )

    try:
        run_query(query, parameters)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="tweet id repeat"
        )
    return tweet

#update a specific tweet
@app.put(
    path="/tweet/update/{tweet_id}",
    tags=["Tweets"],
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    response_model=UpdateTweet
)
def update_a_tweet(
    tweet_id: UUID = Path(
    ...
),
tweet: UpdateTweet = Body(...)
):

    """
        Update a tweet

        This path operation update a specific tweet in the app

        Parameters:\n
            - tweet_id: UUID
            - Request body parameters
                - tweet: Tweet

        Return a json list with the tweet info in the app, with the following keys\n
            - tweet_id: UUID
            - content: str
            - updated_at: datetime
            - by: User
    """

    get_tweet_dict(tweet_id)

    tweet.updated_at = datetime.now()

    query = f"""UPDATE tweet SET 
    content='{tweet.content}',
    updated_at='{tweet.updated_at}'
    WHERE tweet_id='{tweet_id}' """

    run_query(query)

    return tweet

#delete a specific tweet
@app.delete(
    path="/tweet/delete/{tweet_id}",
    tags=["Tweets"],
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    response_model=Tweet
)
def delete_a_tweet(tweet_id: UUID = Path(
    ...
)):

    """
        Delete a tweet

        This path operation delete a specific tweet in the app

        Parameters:\n
            - tweet_id: UUID

        Return a json list with the tweet info in the app, with the following keys\n
            - tweet_id: UUID
            - content: str
            - created_at: datetime
            - updated_at: datetime
            - by: User
    """

    dict_resp = get_tweet_dict(tweet_id)

    query = f"DELETE FROM tweet WHERE tweet_id='{tweet_id}'"
    run_query(query)
    return dict_resp