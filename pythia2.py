from random import random
from dotenv import load_dotenv
from evm import evmDBChat
import pandas as pd
import gradio as gr
import os

# load environment variables from .env.list
load_dotenv()

user = os.getenv("MARIADB_USER")
password = os.getenv("MARIADB_PASS")
host = os.getenv("MARIADB_HOST")
port = os.getenv("MARIADB_PORT")
database = os.getenv("MARIADB_DBASE")

open_ai_key = os.getenv("OPENAI_API_KEY")
gpt_model = os.getenv("model-gpt3")
temperature = float(os.getenv("temperature"))
dburl = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"

config_dict = {
    "user": user,
    "password": password,
    "host": host,
    "port": port,
    "database": database,
    "open_ai_key": open_ai_key,
    "gpt_model": gpt_model,
    "temperature": temperature,
    "dburl": dburl
}


# Load chat interface
def pythiaChat(message, history):
    return


def respond(message, chat_history):
    # call SQLChain
    evm_chat = evmDBChat.evmDBChat(config_dict)

    bot_message = evm_chat.chatEvmDb(message)
    chat_history.append((message, bot_message))
    explain = evm_chat.explanation
    return "", chat_history, explain


with gr.Blocks() as demo:
    with gr.Tab("PM Agent"):
        chatbot = gr.Chatbot()
        msg = gr.Textbox()
        explanation = gr.Textbox(label="Explanation")
        clear = gr.ClearButton([msg, chatbot])

        msg.submit(respond, [msg, chatbot], [msg, chatbot, explanation])

demo.launch(server_name="0.0.0.0")
