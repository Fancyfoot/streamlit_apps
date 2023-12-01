import asyncio
import os
import openai
import streamlit as st
from aiconfig import AIConfigRuntime, InferenceOptions

# Streamlit Setup
st.set_page_config(
    page_title="GPT4 Prompt Routing Demo 🔀",
    page_icon="㏐",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)
st.title("GPT4 Prompt Routing Demo 🔀")
st.subheader("Powered by AIConfig ⚙️")
st.markdown("This is a demo of prompt routing with AIConfig ([Github](https://github.com/lastmile-ai/aiconfig)). Instructions:")

st.text(
    """
    1. Ask a question with a code snippet or specify language in your prompt.  
    For this demo, only python, javascript, java prompt templates were created. 
    2. Router determines programming language and responds with respective prompt template.
    """
)
st.markdown("Try this: `How do I filter a list of numbers to only even numbers in javascript?`")
openai_api_key = st.text_input('First, enter you OpenAI API Key. Uses GPT4.', type='password')


# Get assistant response based on user prompt (prompt routing)
async def assistant_response(prompt):
    params = {"coding_question": prompt}

    router_prompt_completion = await config.run("router", params)
    router_output = config.get_output_text("router")

    if router_output == 'python':
        prompt_completion = await config.run('python_assistant', params)
        response = config.get_output_text('python_assistant')
        return(response)
    if router_output == 'javascript':
        prompt_completion = await config.run('js_assistant', params)
        response = config.get_output_text('js_assistant')
        return(response)
    if router_output == 'java':
        prompt_completion = await config.run('java_assistant', params)
        response = config.get_output_text('java_assistant')
        return(response)
    else: 
        return router_output

if openai_api_key:
    # AI Config Setup
    openai.api_key = openai_api_key
    path = os.path.dirname(__file__)
    my_file = path+'/assistant_aiconfig.json'
    config = AIConfigRuntime.load(my_file)

    # Chat Setup
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a coding question"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        chat_response = asyncio.run(assistant_response(prompt))

        response = f"AI: {chat_response}"

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
