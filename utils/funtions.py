import sqlite3 as sql3
from fastapi import HTTPException, status

"""These are functions that are used repeatedly."""

def run_query(query, parameters = ()):
    """
        Run query

        It is to execute a query against the database.

        Parameters:     
            - query: str
            - parameters: Tuple

        Returns the response of the query.
    """

    #Connect to the database
    with sql3.connect('./database.db') as Connection: 
        cursor = Connection.cursor()
        #Run the query
        response = cursor.execute(query, parameters)
        #confirm the query, to make it permanent
        Connection.commit()
        return response


def get_list(query, func):

    """
        Get list

        It makes a query and transforms its response into a list,
        where each element of the response has been transformed
        into a dictionary by a function and added to the list

        Parameters:     
            - query: str
            - func: function
        
        returns a list of dictionaries
    """

    list_resp = []

    resp = run_query(query)
    for ele in resp:
        list_resp.append(func(ele))

    return list_resp


def user_dict(values=()):

    """
        User dict

        It is to convert a tuple into a dictionary

        Parameters:
            - values: Tuple

        Returns a dictionary with the user information
            - user_id: UUID
            - email: str
            - user_name: str
            - first_name: str
            - last_name: str
            - birth_date: date
    
    """

    dict_user = {
        "user_id": values[0],
        "email": values[1],
        "user_name": values[2],
        "first_name": values[3],
        "last_name": values[4],
        "birth_date": values[5]
    }
    
    return dict_user

def verify_user_existence(query, message):

    """
        Verify user's existence

        It is to verify the existence of a user in the database by a query

        Parameters:
            - query: str
            - message: str

        Returns a dictionary with the user information
            - user_id: UUID
            - email: str
            - user_name: str
            - first_name: str
            - last_name: str
            - birth_date: date
    
    """

    resp = run_query(query)

    try:
        user_info = user_dict(resp.fetchall()[0])
        return user_info
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message
        )

def get_user_dict(user_id):
    """
        Get user dict

        It is to select a user of the database by its id
       
        Parameters:
            - user_id: UUID

        Returns a dictionary with the user information
            - user_id: UUID
            - email: str
            - user_name: str
            - first_name: str
            - last_name: str
            - birth_date: date
    
    """
    query=f"SELECT * FROM user WHERE user_id='{user_id}'"
    message = "This user does not exist"

    user_info = verify_user_existence(query,message)
    return user_info
    

def tweet_dict(values=()):

    """
        Tweet dict

        It is to convert a tuple into a dictionary

        Parameters:
            - values: Tuple

        Returns a dictionary with the tweet information
            - tweet_id: UUID
            - content: str
            - created_at: date
            - update_at: date
            - by: User
    
    """

    dict_user = get_user_dict(values[1])

    tweet_info = {
        "tweet_id":values[0],
        "content": values[3],
        "created_at": values[4],
        "updated_at": values[5],
        "by":dict_user
    }

    return tweet_info



def get_tweet_dict(tweet_id):

    """
        Get tweet dict

        It is to select a tweet of the database and convert into a dictionary

        Parameters:
            - tweet_id: UUID

        Returns a dictionary with the tweet information
            - tweet_id: UUID
            - content: str
            - created_at: date
            - update_at: date
            - by: User
    
    """

    query = f"SELECT * FROM tweet WHERE tweet_id='{tweet_id}'"
    resp = run_query(query)

    try:
        tweet_info = tweet_dict(resp.fetchall()[0])
        return tweet_info
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This tweet does not exist"
        )

