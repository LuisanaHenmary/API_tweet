import sqlite3 as sql3

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

def tweet_dict(values=()):

    """
        Tweet dict

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

    query=f"""SELECT * FROM user WHERE user_id='{values[1]}' """

    resp = run_query(query=query)
    
    for r in resp:
        dict_rest = user_dict(r)

    return {
        "tweet_id":values[0],
        "content": values[3],
        "created_at": values[4],
        "updated_at": values[5],
        "by":dict_rest
    }