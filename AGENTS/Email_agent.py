from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

import smtplib
from logger import get_logger
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json
import sys 
from pathlib import Path
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.tools import StructuredTool



sys.path.insert(0, str(Path(__file__).parent.parent))
        
load_dotenv()

app_pass = os.getenv("APP_PASSWORD")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
logger = get_logger(__name__)
        
if not GROQ_API_KEY:
    logger.error("❌ GROQ_API_KEY not found in .env file")
    raise ValueError("GROQ_API_KEY is required")
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)

sys.stdout.reconfigure(encoding="utf-8")

class Email_schema(BaseModel):
    subject: str = Field(description="Subject of mail")
    body: str = Field(description="Body of mail")


class Email_agent:
    def __init__(self, llm, parser):
        self.llm = llm 
        self.parser = parser
        self.format_instructions = self.parser.get_format_instructions()

    def mail_sender(self ,query: str, receiver_mail: str):
        """Generate and send a professional email based on the query to the specified receiver."""

        if not app_pass:
            logger.error("❌ APP_PASSWORD not found in .env file")
            raise ValueError("APP_PASSWORD is required for Gmail SMTP")
        
        try:
            # Validate inputs
            if not query or not query.strip():
                raise ValueError("Query cannot be empty")
            if not receiver_mail or not receiver_mail.strip():
                raise ValueError("Receiver email address is required")
            if "@" not in receiver_mail:
                raise ValueError("Invalid email address format")
            
            sender_email = "gameranurag24@gmail.com"
            logger.info(f"Generating email for query: {query}")
            logger.info(f"Sending email to: {receiver_mail}")

            llm_prompt = f"""
    You are a professional email writer.

    Generate a professional email in this JSON format:

    {self.format_instructions}

    Topic/Query: {query}

    example-
    Dear Boss,

    I hope you are well. I am writing to request a leave of absence for five days, from Monday to Friday, due to personal matters that require my immediate attention. I have ensured that all my current tasks are up to date, and I will be reachable by email for any urgent issues. I will also coordinate with the team to ensure a smooth workflow during my absence.

    Thank you for your understanding and consideration.

    Sincerely,
    [Your Name]
    use example format
    """

            logger.info("Invoking LLM to generate email...")
            response = self.llm.invoke(llm_prompt)

            try:

                data = self.parser.parse(response.content)

            except json.JSONDecodeError:

                logger.warning("Failed to parse JSON")

                data = {
                    "subject": "Generated Email",
                    "body": response.content
                }

            subject = data["subject"]
            body = data["body"]

            # Create email
            msg = MIMEMultipart()

            msg["From"] = sender_email
            msg["To"] = receiver_mail
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            # SMTP Server
            logger.info(f"Connecting to Gmail SMTP server...")
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                logger.info("Starting TLS...")
                server.starttls()
                logger.info(f"Logging in as {sender_email}...")
                server.login(sender_email, app_pass)
                logger.info(f"Sending email to {receiver_mail}...")
                server.send_message(msg)
                logger.info("✅ Email sent successfully")

            return f"""
    ✅ Email Sent Successfully

    To: {receiver_mail}

    Subject:
    {subject}

    Body:
    {body}
    """

        except Exception as e:

            logger.error(f"Email sending failed: {str(e)}", exc_info=True)

            return f"❌ Error: {str(e)}"
        
email_agent = Email_agent(llm, parser=JsonOutputParser(pydantic_object=Email_schema))

send_email_tool = StructuredTool.from_function(
    func=email_agent.mail_sender,
    name="send_email",
    description="Generate and send a professional email based on query"
)
        
        
agent = create_agent(
    model = llm,
    tools=[send_email_tool],
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "send_email":{
                    "allowed_decisions":["approve","edit","reject"]
                }
            }
        )
    ]
)        
        
        
        
