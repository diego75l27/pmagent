# Module Imports
from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain_experimental.sql import SQLDatabaseChain
import json


class evmDBChat:
    def __init__(self, config_dict):
        self.db = SQLDatabase.from_uri(config_dict["dburl"])
        self.config_dict = config_dict
        self.explanation = ""

    def chatEvmDb(self, message):
        llm = OpenAI(temperature=self.config_dict["temperature"], verbose=True,
                     openai_api_key=self.config_dict["open_ai_key"])

        db_chain = SQLDatabaseChain.from_llm(llm, self.db, verbose=True, return_intermediate_steps=True)
        result = db_chain(message)
        self.explanation = self.extractExplanation(result["intermediate_steps"])
        return result['result']


    def extractExplanation(self, result_set):
        output = result_set[1]
        return output
