from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from tavily import TavilyClient
from dotenv import load_dotenv
import os  

from logger import get_logger 

logger = get_logger(__name__)

class research_agent:
    """
    Research Agent - searching agent for live or updated knowledge that are not feed in LLMs
    """
    
    def __init__(self):
        load_dotenv()
        TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
        if not TAVILY_API_KEY:
            logger.critical("Missing API Key")
            raise ValueError("Missing API key")

        self.client = TavilyClient(api_key=TAVILY_API_KEY)
    
    def websearch_agent(self, query:str):
        """
        Normal Search Agent to search simple querys in basic depth

        Returns:
            _type_: Search Results For Query at basic level
        """
        
        PROMPT = f'''
        you are a ***helpful websearching assistant*** 
        search this query
        ***{query}***
        '''
        
        response = self.client.search(PROMPT, search_depth="basic")
        if not response:
            logger.error("Response not generated")
        else:
            final_response = "\n\n".join([r["content"] for r in response["results"]]) if response.get("results") else ""
            logger.info("Websearch Generated")
            return final_response
        
    def deepsearch_agent(self, query:str):
        """
        It's a DeepSearching Agent for Complex Querys to search in Advanced depth

        Returns:
            _type_: Deep Search Report
        """
        
        PROMPT = f'''
        you are a helpful ***deep reseach agent***
        research this query
        ***{query}***
        '''
        
        response = self.client.search(PROMPT, search_depth="advanced")
        if not response:
            logger.error("Response not generated")
        else:
            final_response = "\n\n".join(
            item.get("content", "")
            for item in response
        )
            logger.info("Deep Search Generated")
            return final_response
    
    def QA_based_search(self, query: str, search_depth: str = "advanced"):

        PROMPT = f"""
        You are a helpful Q&A research agent.

        Research this query:
        {query}
        """

        try:
            response = self.client.qna_search(
                PROMPT,
                search_depth=search_depth
            )

            # DEBUG
            print("RESPONSE:", response)
            print("TYPE:", type(response))

            # If response is plain string
            if isinstance(response, str):
                logger.info("String response generated")
                return response

            # If response is dictionary
            elif isinstance(response, dict):

                results = response.get("results", [])

                final_response = "\n\n".join(
                    item.get("content", "")
                    for item in results
                )

                return final_response

            else:
                return "Unsupported response format"

        except Exception as e:
            logger.exception(e)
            return str(e)