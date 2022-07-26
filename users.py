import pandas as pd
import get_env_variables
import sqlalchemy
import bcrypt

"""This module is used to handle user authentification by interacting between Streamlit app input and PostgreSQL database
"""

def hash_password(password):
    """This function uses bcrypt to return a hashed password from the 
        plain texte password given as input

    Args:
        password (string): password in plain text

    Returns:
        hashed_password (string): hashed password
    """
    hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
    hashed_password = bytes.decode(hashed_password)
    return hashed_password
    
#https://realpython.com/prevent-python-sql-injection/#passing-safe-query-parameters
def add_user(username, password):
    """This functions adds a new user to the database (users table):
        The password is hashed before persistance

    Args:
        username (string): username
        password (string): password in plain text
    """
    hashed_password = hash_password(password)
    engine = sqlalchemy.create_engine(get_env_variables.DATABASE_URI, echo=True)
    engine.execute('INSERT INTO users(username, password) VALUES (%s,%s)', (username, hashed_password))
    


def check_user_already_exists(username):
    """This function is used to ckeck whether the username choosen by a new user for an account creation does already exist in the database. 

    Args:
        username (string): username as the user input of the sign up form

    Returns:
        Bool: True if user already exists, else False
    """
    engine =  sqlalchemy.create_engine(get_env_variables.DATABASE_URI, echo=True)
    result = engine.execute("SELECT username from users WHERE username = %s", (username))
    result_list = [r[0] for r in result]
    result = (len(result_list) != 0)
    return result


def check_password(username, password):
    """This function is used to compare, for a given username, the input password 
        to the one stored in the database, both beeing hashed using bcrypt

    Args:
        username (string): username used by user to login and stored in the database
        password (string): password used to login associated with username 
            and stored after hashing in database

    Returns:
        Bool: True if input password is the same as the expected password 
        (the one stored into the database for this username)
        False if it is not or if user name not found.
    """
    engine = sqlalchemy.create_engine(get_env_variables.DATABASE_URI, echo=True)
    # retrieve db password
    result = engine.execute("SELECT password from users WHERE username = %s", (username))
    try:
        result_list = [r[0] for r in result]
        db_password = str.encode(result_list[0])
        # compare input password to db password
        check = bcrypt.checkpw(str.encode(password), db_password)
        return check
    except:
        return False






