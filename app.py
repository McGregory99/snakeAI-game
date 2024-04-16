import streamlit as st

from agent import train

st.set_page_config(page_title='SNAKE AI GAME',
        page_icon=":snake", 
        layout='centered', 
        initial_sidebar_state='expanded')

if __name__ == '__main__':
    train()