
import requests
import pandas as pd
import json
import base64

import streamlit as st

import users

# lien à faire avec FastAPI
# http://127.0.0.1:8000 is endpoint from fastapi
#response = requests.post("http://127.0.0.1:8000/predict")
#st.write(response)


# ---- CONTAINERS DECLARATION ----
header_section = st.container()
main_section = st.container()
login_section = st.expander("LOG IN")
logout_section = st.sidebar.container()
signup_section = st.expander("SIGN UP")


# ---- UTILS ----
# from https://levelup.gitconnected.com/how-to-add-a-background-image-to-your-streamlit-app-96001e0377b2

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )


# ---- PREDICTION ----
def show_prediction_page():
    """This functions shows prediction page :
            - imput form for features
            - API call
            - prediction output
    """
    st.header("PREDICTION ZONE")
    form_col, output_col = st.columns(2)
    # input form
    with form_col:
        with st.form(key="input form"):
            st.subheader('Select values for features :')
            dettes = st.slider("Dettes")
            statut = st.selectbox(
                'Quel statut ?', 
                ('Société à responsabilité limitée (SARL)', 'Société par actions simplifiée', "Société anonyme à conseil d'administration", "Entrepreneur individuel"))
            ape = st.selectbox(
                'Quel secteur ?', 
                ('A', 'B', 'C', 'D', 'E' 'F', 'G'))
            submitted = st.form_submit_button("Submit")
    # prediction output
    with output_col:
        if submitted:
            payload = {"dettes":dettes,"statut":statut,"APE":ape}
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            response = requests.post("http://127.0.0.1:8000/predict", headers=headers, json=payload)
            result = response.json()
            if result['pred'] == 'wont fail':
                st.subheader("Prediction : Won't fail")
                st.image("001-yes.png")
                st.caption(f"failure probability : {round(result['failure_proba']*100, 2)}%")
            else:
                st.subheader("Prediction : Will fail")
                st.image("003-no.png")
                st.caption(f"failure probability : {round(result['failure_proba']*100, 2)}%")


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

