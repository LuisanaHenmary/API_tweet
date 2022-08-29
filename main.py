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
        run_query("INSERT INTO user VALUES(?,?,?,?,?,?,?)", parameters)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This user does exist"
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

    query = """SELECT user_id,
    email,
    user_name,
    first_name,
    last_name,
    birth_date,
    password
    FROM user"""

    list_user = []

    resp = run_query(query=query)
    for ele in resp:
        list_user.append(user_dict(ele))

    return list_user

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
        description="This is person id, it is greter or equal to 0",
        example=999
    )):
    query = f"""SELECT user_id,
    email,
    user_name,
    first_name,
    last_name,
    birth_date,
    password
    FROM user WHERE user_id='{user_id}' """

    resp = run_query(query=query)
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
        description="This is person id, it is greter or equal to 0",
        example=999
    ),
    user: UserRegister = Body(...)
    ):

    query = f"""UPDATE user SET 
    user_name='{user.user_name}',
    password='{user.password}'
    WHERE user_id='{user_id}' """

    run_query(query=query)

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
        description="This is person id, it is greter or equal to 0",
        example=999
    )):

    query = f"""SELECT user_id,
    email,
    user_name,
    first_name,
    last_name,
    birth_date,
    password
    FROM user WHERE user_id='{user_id}' """

    resp = run_query(query=query)
    for ele in resp:
        dict_resp = user_dict(ele)

    query = f"DELETE FROM user WHERE user_id='{user_id}'"
    run_query(query=query)
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
    query = """SELECT tweet_id,
    user_id,
    user_name,
    content,
    created_at,
    updated_at
    FROM tweet"""

    list_tweet = []

    resp = run_query(query=query)
    for ele in resp:
        list_tweet.append(tweet_dict(ele))

    return list_tweet

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

    parameters = (
        str(tweet.tweet_id),
        str(tweet.by.user_id),
        tweet.by.user_name,
        tweet.content,
        str(tweet.created_at),
        str(tweet.updated_at)
    )

    try:
        run_query("INSERT INTO tweet VALUES(?,?,?,?,?,?)", parameters)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="tweet repeat"
        )
    return tweet