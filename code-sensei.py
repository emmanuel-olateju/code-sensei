import streamlit as st
import time
from streamlit_option_menu import option_menu
import os
import openai

openai.api_key = os.getenv("CODE_SENSEI_OPENAI_KEY")

def generate_code_and_explanation(prompt):
    response = openai.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=prompt
    )
    return  response.choices[0].message.content

def set_chat_history():
    pass

def load_past_chats():
    st.session_state['past_chats'] = ['Empty Tinker']*10

if 'chat_just_starting' not in st.session_state:
    st.session_state['chat_just_starting'] = True

if 'chatting_status' not in st.session_state:
    st.session_state.chatting_status = False

if 'selected_chat_history' not in st.session_state:
    st.session_state.selected_chat_history = None

if st.session_state.selected_chat_history==None:
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [[],[],[],[]]
        st.session_state.messages = []
    else:
        st.session_state.selected_chat_history = 'New Chat'
else:
    set_chat_history()


def chatting():
    st.session_state.chatting_status = True

def switch_to_chat_page():
    st.switch_page("./pages/chat.py")

def signup():
    signup_sidebar = st.sidebar
    with signup_sidebar:
        st.session_state.email = st.text_input('email',key='signup_email')
        st.session_state.name = st.text_input('name')
        st.session_state.username = st.text_input('username')
        st.session_state.education = st.selectbox('Education Level',['','Primary','Secondary','Undergraduate','Post-graduate'])
        st.session_state.track = st.selectbox('Preferred Track',['','Software Engineering','Data Science','DevOps','Cyber Security'])
        st.session_state.user_language = st.selectbox('Primary Language',['','Python','C#','C++','C','Javascript','Pseudocode'])
        #Temprorary
        st.session_state.user_language = 'python'
        col1, col2, col3 = st.columns([0.33]*3)
        with col2:
            st.button('Sign Up',on_click=chatting,key='sign_up')

def login():
    #Temprorary
    st.session_state.user_language = 'python'
    login_sidebar = st.sidebar
    with login_sidebar:
        st.session_state.email = st.text_input('email',key='login_email')
        col1, col2, col3 = st.columns([0.33]*3)
        with col2:
            st.button('Log In',on_click=chatting,key='log_in')

st.set_page_config(
    page_title="🧠 code-sensei",
    page_icon="",
)

def main():
    load_past_chats()
    if st.session_state.chatting_status==False:
        ct1 = st.container(height=200,border=False)
        ct2 = st.container(height=110,border=False)
        ct3 = st.container(height=240,border=False)
        with ct3:
            cols = st.columns([0.32,0.3,0.18])
            with cols[1]:
                st.image('6.jpg',width=100)
            col1, col2, col3 = st.columns([0.38,0.32,0.4])
            with col2:
                st.markdown('## code-sensei')
            col1, col2, col3, col4, col5, col6 = st.columns([0.167]*6)
            with col3:
                st.button("Log In",on_click=login)
            with col4:
                st.button("Sign Up",on_click=signup)
        ct4 = st.container(height=100,border=False)
        ct5 = st.container(height=100,border=False)
    else:
        with st.sidebar:
            st.button('New Tinker')
            st.session_state.selected_chat_history = option_menu('Old chats',st.session_state.past_chats)
        st.session_state.chat_input = st.chat_input('What do you want your code to do?')
        if st.session_state.chat_just_starting==True:
            cols = st.columns([0.2]+([0.1]*8))
            st.container(height=170,border=False)
            ct = st.container(height=200,border=False)
            with ct:
                cols = st.columns([0.3,0.3,0.2])
                with cols[1]:
                    st.image('6.jpg',width=100)
                cols = st.columns([0.03,0.93,0.04])
                with cols[1]:
                    st.markdown('#### I\'d love to help you learn and interprete codes faster')
            st.session_state.chat_just_starting = False
            print('Here')
        else:
            print('chat_started')
            if st.session_state.chat_input!=None:
                st.session_state.messages.append(st.session_state.chat_input)
                prompt = f'Write a {st.session_state.user_language} code that {st.session_state.chat_input} and then explain it'
                st.session_state.chat_history[0].append({
                    'role':'user',
                    'content':prompt
                })
                code_snippet = generate_code_and_explanation(st.session_state.chat_history[0])
                st.session_state.chat_history[1].append({
                    'role':'ai',
                    'content':code_snippet
                })

                prompt = f'In an explicit manner towards a 3 year old child, explain what each line of the code below does \n {code_snippet} \
                with reference to the line number of each  line in the code'
                st.session_state.chat_history[2].append({
                    'role':'user',
                    'content':prompt
                })
                code_explaination = generate_code_and_explanation(st.session_state.chat_history[2])
                st.session_state.chat_history[3].append({
                    'role':'ai',
                    'content':code_explaination
                })
                
                print('length of chat history:{}'.format(len(st.session_state.chat_history)))
                for message_index,message in enumerate(st.session_state.chat_history[0]):
                    with st.chat_message(message['role']):
                        st.markdown(st.session_state.messages[message_index])
                    with st.chat_message(st.session_state.chat_history[1][message_index]['role']):
                        st.code(st.session_state.chat_history[1][message_index]['content'],language=st.session_state.user_language,line_numbers=True)
                        st.markdown(st.session_state.chat_history[3][message_index]['content'])


if __name__=='__main__':
    main()