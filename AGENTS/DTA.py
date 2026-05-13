from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_groq import ChatGroq
import os   
from dotenv import load_dotenv
from logger import get_logger

logger = get_logger(__name__)

class DTA_BOT:
    """
    Data Analyst for Analyzing the csv files
    """
    
    def __init__(self, model:str = "llama-3.3-70b-versatile"):
        load_dotenv()
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        if not GROQ_API_KEY:
            logger.critical("Missing API Key")
            raise ValueError("Missing Api key")
        
        self.model = model
        self.client = ChatGroq(model=self.model)
        
    def Analyse(self, df_info, query):
        """
        Analysis work here

        Args:
            df_info (_type_): String
            query:String
        """

        PROMPT = f'''
       Dataset info
       
       {df_info}

    Query-
    {query}
Task:
Analyze trends, anomalies, risks, and business insights.
Suggest next actions.
        '''
        
        response = self.client.invoke(PROMPT)
        if not response:
            logger.error("Response not generated")
        else:
            logger.info("Analytics generated")
            return response.content
            
        
        