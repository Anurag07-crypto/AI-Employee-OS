from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_core.messages import HumanMessage
from datetime import datetime
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import requests
import os
from logger import get_logger

logger = get_logger(__name__)

class State(TypedDict):
    messages:Annotated[list, add_messages]

def calculator(expression: str):
    """Evaluate a mathematical expression."""
    return eval(expression)

def get_time():
    """Get current system time."""
    return datetime.now().strftime("%H:%M:%S")

def weather(city):
    """Get current weather for the city"""

    API_KEY = os.getenv("weather_api_key")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    data = response.json()

    if response.status_code == 200:

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"]

        return f"""
Weather in {city}

🌡 Temperature: {temp}°C
💧 Humidity: {humidity}%
☁ Condition: {condition}
"""

    else:
        return "City not found"


tools = [calculator, weather, get_time]

def Normal_agent(state:State, model:str="llama-3.3-70b-versatile"):
    """
    Normal agent for basic tasks
    """
    
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        logger.critical("Missing API Key")
        raise ValueError("Missing API key")
    
    llm = ChatGroq(model=model)
    llm_with_tools = llm.bind_tools(tools=tools)
    response = llm_with_tools.invoke(state["messages"])
    
    logger.info("Normal agent response generated")
    
    return {"messages": [response]}

graph_builder = StateGraph(State)
tool_node = ToolNode(tools)
graph_builder.add_node("normal_agent",Normal_agent)
graph_builder.add_edge(START, "normal_agent")
graph_builder.add_node("tools", tool_node)
graph_builder.add_edge("tools","normal_agent")
graph_builder.add_conditional_edges(
    "normal_agent",
    tools_condition
)
graph_builder.add_edge("tools",END)
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

config = {"configurable":{"thread_id":"1"}}

def get_response(query:str):

    response = graph.invoke(
        {"messages": [HumanMessage(content=query)]},
        config=config
    )
    
    return response["messages"][-1].content

