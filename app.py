import streamlit as st
import pandas as pd
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "True"
os.environ["LANGCHAIN_PROJECT"] = "Q&A Chatbot With OpenAI"

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user's queries"),
        ("user", "Question:{question}"),
    ]
)

def generate_response(question, api_key, llm, temperature, max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(model=llm, openai_api_key=api_key)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({"question": question})
    return answer

# Title of the Streamlit App
st.title('Q&A Chatbot With OpenAI')

# Sidebar
st.sidebar.title('Settings')
api_key = st.sidebar.text_input('Enter your OpenAI API Key:', type='password')

# Dropdown for Language Models
llm = st.sidebar.selectbox('Select OpenAI Language Model:', ['gpt-3.5-turbo', 'gpt-4o-mini'])

# Slider for Temperature and Max Tokens
temperature = st.sidebar.slider('Temperature:', min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider('Max Tokens:', min_value=50, max_value=500, value=100)

# Main Interface
st.write("Ask a question to the Chatbot")
user_input = st.text_input("You:")

if api_key:
    if user_input:
        response = generate_response(user_input, api_key, llm, temperature, max_tokens)
        st.write(response)
    else:
        st.write("Ask a question to the Chatbot")
else:
    st.write("Please enter your OpenAI API Key in the settings.")
