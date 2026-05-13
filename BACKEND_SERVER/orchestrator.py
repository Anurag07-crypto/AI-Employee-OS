from AGENTS.Coding_agent import coding_assistant
from AGENTS.DTA import DTA_BOT
from AGENTS.Research_agent import research_agent
from AGENTS.DEFAULT_agent import get_response
from AGENTS.Email_agent import agent

AGENTS = {

    "code_debugger":
        coding_assistant().code_debugger,

    "code_explainer":
        coding_assistant().code_explainer,

    "code_reviewer":
        coding_assistant().code_reviewer,

    "dta_bot":
        DTA_BOT().Analyse,

    "websearch_agent":
        research_agent().websearch_agent,

    "deepsearch_agent":
        research_agent().deepsearch_agent,

    "question_&_answer_agent":
        research_agent().QA_based_search,

    "default_agent":
        get_response,

    "email_agent":
        agent
}

AGENT_TYPES = {

    "email_agent": "interactive",

    "code_debugger": "normal",

    "default_agent": "normal",

    "deepsearch_agent": "normal",
    
    "code_explainer": "normal",
    
    "code_reviewer": "normal",
    
    "websearch_agent": "normal",
    
    "question_&_answer_agent": "normal",
    
    "dta_bot": "two_info"
}