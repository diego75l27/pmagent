from random import random
from dotenv import load_dotenv
import pandas as pd
import gradio as gr
import os
import neo4jCSVUploader

# load environment variables from .env.list
load_dotenv()


# Load chat interface
def pythiaChat(message, history):
    return random.choice(["Yes", "No"])


# Neo4j configuration
uri = os.getenv('GRAPHDB_URI')
username = os.getenv('GRAPHDB_USER')
password = os.getenv('GRAPHDB_PASS')


# Instantiate the Neo4jCSVUploader class
uploader = neo4jCSVUploader.Neo4jCSVUploader(uri, username, password)


with gr.Blocks() as iface:
    with gr.Tab("Upload Nodes"):
        inp = gr.File()
        uploadNodes = gr.Button(value="Submit")
        out = gr.Textbox()
        uploadNodes.click(
            fn=uploader.process_upload,
            inputs=inp,
            outputs=out
        )
    with gr.Tab("Upload Relationship"):
        gr.Button("New Tiger")


iface.launch()
