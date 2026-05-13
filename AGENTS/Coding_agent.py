from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_groq import ChatGroq
import os  
from dotenv import load_dotenv
from logger import get_logger 

logger = get_logger(__name__)

class coding_assistant:
    """
    A Coding assistant for coding related querys
    """
    
    def __init__(self,model:str="qwen/qwen3-32b"):
        load_dotenv()
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        if not GROQ_API_KEY:
            logger.critical("Missing API Key")
            raise ValueError("Missing API Key")
        
        self.model = model
        self.client = ChatGroq(model=self.model)
        
    def code_debugger(self, query):
        """
        A debugger for your Debugging Problems

        Returns:
            _type_: debugging solution
        """
        
        PROMPT = f'''
        You are a helpful ***code debugger*** with ***10+ years of experience***, whenever you got a 
        query you have to help to debug this code then you have to do it like a senior
        QUERY-
        ***{query}***
        -----------------------
        Make sure seperate ***code blocks*** when answered
        don't give thinking part in response
        '''
        
        response = self.client.invoke(PROMPT)
        logger.info("Code Debugger response generated")
        return response.content
    
    def code_explainer(self, query):
        """
        An Explainer for in you to helping to tackle coding related querys

        Returns:
            _type_: An Explaination
        """
        
        PROMPT = f'''
        You are a helpful ***code explainer*** with ***10+ years of experience***, whenever you got a 
        query to you have to explain why it's failing and what should be the Solution
        QUERY-
        ***{query}***
        -----------------------
        Make sure You Explain Query Like an Expert or in Professional Way
        don't give thinking part in response
        '''
        
        response = self.client.invoke(PROMPT)
        logger.info("Code Explainer response generated")
        return response.content
    
    def code_reviewer(self, query):
        """
        A Code Reviver To Review your given code with Being Brutally Honest

        Returns:
            _type_: Code Review
        """
        
        PROMPT = f'''
        You are a helpful ***Code reviewer*** with over ***10+ years*** experience 
        whenever a user send you thier code you have to ***brutally review*** thier code 
        and ***give suggestions to where to fix*** 
        QUERY-
        ***{query}***
        ---------------------
        Make sure you review very effeciently
        don't give thinking part in response
        '''
        
        response = self.client.invoke(PROMPT)
        logger.info("Code Reviewer response generated")
        return response.content
    