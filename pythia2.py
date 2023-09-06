from random import random
from dotenv import load_dotenv
import pandas as pd
import gradio as gr
import os
import evmDBChat

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
    evmChat = evmDBChat.evmDBChat(config_dict)
    return evmChat.chatEvmDb(message)



with gr.Blocks() as iface:
    with gr.Tab("Q&A SQL Data"):
        gr.ChatInterface(
            fn=pythiaChat,
            title="EVM Agent",
            description="Your Project Management Agent for Enhanced Productivity",
        )

iface.launch(share=TRUE)
