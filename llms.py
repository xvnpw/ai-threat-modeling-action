from langchain.chat_models import ChatOpenAI
import constants
import os

class LLMWrapper:
    def __init__(self, args):
        self.args = args
        
    def create(self) -> ChatOpenAI:
        if self.args.provider == "openrouter":
            openai_api_key=os.environ.get(constants.OPENROUTER_API_KEY)
            openai_api_base=constants.OPENROUTER_API_BASE
            headers={"HTTP-Referer": constants.OPENROUTER_REFERRER}
            
            return ChatOpenAI(temperature=self.args.temperature, 
                model_name=self.args.model,
                openai_api_key=openai_api_key,
                openai_api_base=openai_api_base,
                headers=headers)
            
        elif self.args.provider == "openai":
            openai_api_key=os.environ.get(constants.OPENAI_API_KEY)
        
            return ChatOpenAI(temperature=self.args.temperature, 
                model_name=self.args.model,
                openai_api_key=openai_api_key)
        