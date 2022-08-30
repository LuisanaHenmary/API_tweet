import sqlite3 as sql3
from fastapi import HTTPException, status

"""These are functions that are used repeatedly."""

def run_query(query, parameters = ()):
    """
        Run query

        It is to execute a query against the database.

        Parameters:     
            - query: String
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

def user_dict(values=()):

    """
        User dict

        It is to convert a tuple into a dictionary

        Parameters:
            - values: Tuple

        Returns a dictionary with the user information
            - user_id: str
            - email: str
            - user_name: str
            - first_name: str
            - last_name: str
            - birth_date: date
    
    """
    
    return {
        "user_id": values[0],
        "email": values[1],
        "user_name": values[2],
        "first_name": values[3],
        "last_name": values[4],
        "birth_date": values[5]
    }

def get_user_dict(user_id):
    query=f"SELECT * FROM user WHERE user_id='{user_id}'"
    resp = run_query(query)

    try:
        return user_dict(resp.fetchall()[0])
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This user does not exist"
        )
    

def tweet_dict(values=()):

    """
        Tweet dict

        It is to convert a tuple into a dictionary

        Parameters:
            - values: Tuple

        Returns a dictionary with the tweet information
            - tweet_id: str
            - content: str
            - created_at: date
            - update_at: date
            - by: User
    
    """

    dict_resp = get_user_dict(values[1])

    return {
        "tweet_id":values[0],
        "content": values[3],
        "created_at": values[4],
        "updated_at": values[5],
        "by":dict_resp
    }

def get_tweet_dict(tweet_id):
    query = f"SELECT * FROM tweet WHERE tweet_id='{tweet_id}'"
    resp = run_query(query)

    try:
        return tweet_dict(resp.fetchall()[0])
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This tweet does not exist"
        )