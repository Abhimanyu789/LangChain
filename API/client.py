import requests
import streamlit as st

import requests

def get_openai_response(input_text):
    try:
        response = requests.post(
            "http://localhost:8000/essay/invoke",
            json={'input': {'topic': input_text}}
        )
        
        # Check if response is valid JSON
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        try:
            data = response.json()  # Try to parse the response as JSON
            return data.get('output', {}).get('content', 'Content not found')
        except ValueError:
            print("Error: Response is not valid JSON")
            print(f"Response: {response.text}")
            return "Error: Invalid response from OpenAI API"
    
    except requests.exceptions.RequestException as e:
        # Handles connection errors, timeouts, etc.
        print(f"Request failed: {e}")
        return "Error: Request to OpenAI API failed"
    

def get_ollama_response(input_text):
    try:
        response = requests.post(
            "http://localhost:8000/poem/invoke",
            json={'input': {'topic': input_text}}
        )
        
        # Check if response is valid JSON
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        try:
            data = response.json()  # Try to parse the response as JSON
            return data.get('output', 'No output found')
        except ValueError:
            print("Error: Response is not valid JSON")
            print(f"Response: {response.text}")
            return "Error: Invalid response from Ollama API"
    
    except requests.exceptions.RequestException as e:
        # Handles connection errors, timeouts, etc.
        print(f"Request failed: {e}")
        return "Error: Request to Ollama API failed"


## streamlit framework

st.title('Langchain Demo With Gemma2 API')
input_text=st.text_input("Write an essay on")
input_text1=st.text_input("Write a poem on")

if input_text:
    st.write(get_openai_response(input_text))

if input_text1:
    st.write(get_ollama_response(input_text1))