# Module Imports
from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain_experimental.sql import SQLDatabaseChain


class evmDBChat:
    def __init__(self, config_dict):
        self.db = SQLDatabase.from_uri(config_dict["dburl"])
        self.config_dict = config_dict

    def chatEvmDb(self, message):
        llm = OpenAI(temperature=self.config_dict["temperature"], verbose=True, openai_api_key=self.config_dict["open_ai_key"])
        db_chain = SQLDatabaseChain.from_llm(llm, self.db, verbose=True)
        output_message = db_chain.run(message)
        return output_message
