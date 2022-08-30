from utils.funtions import (
    run_query,
    user_dict,
    tweet_dict
)

from typing import List

from fastapi import (
    FastAPI,
    status,
    HTTPException,
    Path,
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
    user_id: str = Path(
        ...,
        title="Person id",
        description="This is person id, it is greter or equal to 0"
    )):
    query = f"SELECT * FROM user WHERE user_id='{user_id}'"

    resp = run_query(query)
    for ele in resp:
        dict_resp = user_dict(ele)

    return dict_resp

#updates a specific user
@app.put(
    path="/users/update/{user_id}",
    tags=["Users"],
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Updates a specific user"
)
def update_a_user(
    user_id: str = Path(
        ...,
        title="Person id",
        description="This is person id, it is greter or equal to 0"
    ),
    user: UserRegister = Body(...)
    ):

    query = f"""UPDATE user SET 
    user_name='{user.user_name}',
    password='{user.password}'
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
    user_id: str = Path(
        ...,
        title="Person id",
        description="This is person id, it is greter or equal to 0"
    )):

    query = f"SELECT * FROM user WHERE user_id='{user_id}' "

    resp = run_query(query)
    for ele in resp:
        dict_resp = user_dict(ele)

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
    query = "SELECT * FROM tweet"

    list_tweets = []

    resp = run_query(query)
    for ele in resp:
        list_tweets.append(tweet_dict(ele))

    return list_tweets


#show user tweets
@app.get(
    path="/tweets/{user_id}",
    tags=["Tweets"],
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    response_model=List[Tweet]
)
def show_a_tweet(user_id: str = Path(
    ...
)):
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
def show_a_tweet(tweet_id: str = Path(
    ...
)):
    query = f"SELECT * FROM tweet WHERE tweet_id='{tweet_id}'"

    resp = run_query(query)
    for ele in resp:
        tweet = tweet_dict(ele)

    return tweet

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

        Parameters:
            - Request body parameters
                - tweet: Tweet

        Return a json with the basic tweet information:
            - tweet_id: UUID
            - content: str
            - created_at: datetime
            - updated_at: Optional[datetime]
            - by: User
    """
    query = "INSERT INTO tweet VALUES(?,?,?,?,?,?)"
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

#delete a specific tweet
@app.delete(
    path="/tweet/delete/{tweet_id}",
    tags=["Tweets"],
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    response_model=Tweet
)
def delete_a_tweet(tweet_id: str = Path(
    ...
)):

    query = f"SELECT * FROM tweet WHERE tweet_id='{tweet_id}' "

    resp = run_query(query)
    for ele in resp:
        dict_resp = tweet_dict(ele)

    query = f"DELETE FROM tweet WHERE tweet_id='{tweet_id}'"
    run_query(query)
    return dict_resp

#update a specific tweet
@app.put(
    path="/tweet/update/{tweet_id}",
    tags=["Tweets"],
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    response_model=Tweet
)
def update_a_tweet(
    tweet_id: str = Path(
    ...
),
tweet: Tweet = Body(...)
):
    query = f"""UPDATE tweet SET 
    content='{tweet.content}'
    WHERE tweet_id='{tweet_id}' """

    run_query(query)

    return tweet