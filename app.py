import requests
import pandas as pd
import json
import base64

import streamlit as st

import users
import get_env_variables
from prepare_data import prepare_input

"""This file holds the main file of a Streamlit app used to predict company failure probability
"""

# ---- PAGE SETTINGS ----
#st.set_page_config(page_title="Fail predict", page_icon="crash-1.jpg", layout="centered", initial_sidebar_state="collapsed", menu_items=None)

# ---- CONTAINERS DECLARATION ----
header_section = st.container()
main_section = st.container()
login_section = st.expander("LOG IN")
logout_section = st.sidebar.container()
signup_section = st.expander("SIGN UP")

# ---- PREDICTION ----
def show_prediction_page():
    """This functions shows prediction page :
            - imput form for features
            - API call
            - prediction output
    """
    #prediction input
    st.header("SELECTIONNEZ UNE ENTREPRISE :")
    with st.form(key="input form"):
            company = st.selectbox(
                'Quelle entreprise ?', 
                ("La Dolce Data", "Walking Bread", "World Company", "Tech tonique"))
            submitted = st.form_submit_button("Soumettre")

    #prediction output
    with st.container():
        if submitted:
            # load json file holding features for each choice
            data = json.load(open("data.json"))

            # create 2 tabs to display results
            tab1, tab2 = st.tabs([" 🔮 Prédiction", " 📓 Données détaillées"])

            # tab1 holds prediction
            with tab1:
                payload_2 = data[company]
                headers = {"Content-Type": "application/json", "Accept": "application/json"}
                response = requests.post(get_env_variables.API_URL, headers=headers, json=payload_2)
                result = response.json()
                if result['pred'] == 'wont fail':
                    st.header("Prédiction : PROSPERITE")
                    st.image("001-yes.png", width=80)
                    st.caption(f"probabilité de faillite : {round(result['failure_proba']*100, 2)}%")
                else:
                    st.header("Prédiction : FAILLITE")
                    st.image("003-no.png", width=80)
                    st.caption(f"probabilité de faillite : {round(result['failure_proba']*100, 2)}%")
            # tab2 displays the input data
            with tab2:
                st.header("Données détaillées")
                df = prepare_input(data[company])
                df = df.rename(columns={0:company})
                st.write(df)


# ---- USER AUTHENTIFICATION ----
def logged_out_clicked():
    """This function resets the st.session_state["logged in"] to False 
        when the Log Out button is cliked in order to show login page again
    """
    st.session_state['logged_in'] = False

def show_logout_page():
    """This function shows the logout section in the sidebar
    """
    with logout_section:
        if st.session_state['username']:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image("005-user.png")
            with col2:
                st.subheader(f"Logged as {st.session_state['username']}")
            with col3:
                st.write("")
        col4, col5, col6 = st.columns(3)
        with col4:
            st.write("")
        with col5:
            st.button("Log Out", key="logout", on_click=logged_out_clicked)
        
def logged_in_clicked(username, password):
    """This function uses the users module to check if password 
        entererd by user is the same as the one stored in the
        database for this username. 

        If password is correct, this functions turns st.session_state["logged_in"] 
        to True that allows the user to have access to other pages of the app.
        
        Else an error message is prompted and the login page remains

    Args:
        username (string): input from user
        password (string): input from user
    """
    if users.check_password(username, password):
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
    else:
        st.session_state['logged_in'] = False
        st.error("Invalid user name or password")

def signup_clicked(username, password):
    """This functions allows a new user to create an account. 
            - Controls wether username is free to use
            - If so, adds username and hashed password to database and loggs in the user
            - If not, prompts an error message

    Args:
        username (string): input from user
        password (string): input from user
    """
    if not users.check_user_already_exists(username):
        st.session_state['logged_in'] = True
        users.add_user(username, password)
        st.success("You have successfully created your account")
        st.session_state['username'] = username
    else:
        st.session_state['logged_in'] = False
        st.error("This user name does already exist. Please choose another one")

def show_authentification_page():
    """This function shows the landing page of app, composed by 2 expanders
        allowing user to login or signup
    """
    with login_section:
        if st.session_state['logged_in'] == False:
            st.subheader("Login section")
            username_login = st.text_input("User Name", key="user_login", value="")
            password_login = st.text_input("Password", type="password", value="")
            st.button("Login", on_click=logged_in_clicked, args= (username_login, password_login))
    with signup_section:
        if st.session_state['logged_in'] == False:
            st.subheader("Create a new account")
            username_signup = st.text_input("User Name", key="user_signup", value="")
            password_signup = st.text_input("Choose a password", type="password", value="")
            st.button("Sign Up", on_click=signup_clicked, args=(username_signup, password_signup))


# ---- MAIN ----
with header_section:
    title_col, img_col = st.columns(2)
    with img_col:
        st.image("crash-1.jpg")
    with title_col:
        st.title("Is this company likely to fail ?")
    # first run : initialization of st.session_state
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        show_authentification_page()
    else:
        if st.session_state['logged_in']:
            show_logout_page()
            show_prediction_page()
        else:
            show_authentification_page()

