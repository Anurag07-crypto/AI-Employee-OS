from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from BACKEND_SERVER.orchestrator import AGENTS, AGENT_TYPES
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
import uvicorn
from pydantic import BaseModel
from typing_extensions import Optional
from logger import get_logger
from langgraph.types import Command
from AGENTS.TALKATIVE_agent import Talkie
import base64
import uuid

class Request(BaseModel):
    """
    Schema of the server

    Args:
        BaseModel (_type_): BaseModel
    """
    query:str
    agent:str
    df_info:Optional[str] = None
    thread_id: Optional[str] = None

logger = get_logger(__name__)

app = FastAPI()

AUDIO_UPLOAD_DIR = Path(__file__).parent.parent / "CHAT_HISTORY" / "talkative_uploads"
AUDIO_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.post("/server")
def server(request: Request):
    """
    Taking server request 
    Args:
        request (Request): Request Schema

    Raises:
        HTTPException: RunTime Error in server
        HTTPException: Unicode encoding error in server
        HTTPException: Unexpected error in server

    Returns:
        _type_: string
    """
    try:
        selected_agent = AGENTS[request.agent]
        agent_type = AGENT_TYPES[request.agent]
        
        if agent_type == "normal":
            response = selected_agent(request.query)
            return {
                "status": "completed",
                "response": response
            }
            
        elif agent_type == "interactive":
            response = selected_agent.invoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": request.query
                            }
                        ]
                    },
                    config={
                        "configurable": {
                            "thread_id": request.thread_id
                        }
                    }
                )

            if "__interrupt__" in response:

                return {
                    "status": "approval_required",
                    "interrupt": response["__interrupt__"]
                }

            return {
                  "status": "completed",
                  "response": response
               }
        
        elif agent_type == "two_info":
            response = selected_agent(request.df_info, request.query)
            return {
                "status": "completed",
                "response": response
            }


    except RuntimeError as e:
        logger.error(f"Runtime error in /server: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except UnicodeEncodeError as e:
        logger.error(f"Unicode encoding error in /server: {e}")
        raise HTTPException(status_code=500, detail="Error processing response with special characters")
    except Exception as e:
        logger.error(f"Unexpected error in /server: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Something went wrong. please try again")


@app.post("/talkative")
async def talkative(audio_file: UploadFile = File(...), thread_id: Optional[str] = Form(None)):
    """
    Run the Talkative voice agent from an uploaded audio file.
    """
    try:
        suffix = Path(audio_file.filename or "audio.wav").suffix or ".wav"
        safe_thread_id = thread_id or str(uuid.uuid4())
        upload_path = AUDIO_UPLOAD_DIR / f"{safe_thread_id}_{uuid.uuid4().hex}{suffix}"

        with open(upload_path, "wb") as file:
            file.write(await audio_file.read())

        result = Talkie(str(upload_path)).friend()
        audio_path = Path(result["audio_path"])

        with open(audio_path, "rb") as file:
            audio_base64 = base64.b64encode(file.read()).decode("utf-8")

        return {
            "status": "completed",
            "agent": "talkative_agent",
            "thread_id": safe_thread_id,
            "transcription": result["transcription"],
            "response": result["response"],
            "audio_base64": audio_base64,
            "audio_mime": "audio/wav",
            "metadata": {
                "input_file": audio_file.filename,
                "output_format": "wav"
            }
        }

    except Exception as e:
        logger.error(f"Talkative agent error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

class ApprovalRequest(BaseModel):
    decision: str
    thread_id: str
    edited_content: Optional[str] = None


from langgraph.types import Command

@app.post("/approve")
def approve(request: ApprovalRequest):

    try:

        email_agent = AGENTS["email_agent"]

        # APPROVE
        if request.decision == "approve":

            response = email_agent.invoke(
                Command(
                    resume={
                        "decisions": [
                            {
                                "type": "approve"
                            }
                        ]
                    }
                ),
                config={
                    "configurable": {
                        "thread_id": request.thread_id
                    }
                }
            )

        # EDIT
        elif request.decision == "edit":

            response = email_agent.invoke(
                Command(
                    resume={
                        "decisions": [
                            {
                                "type": "edit",
                                "edited_value": request.edited_content
                            }
                        ]
                    }
                ),
                config={
                    "configurable": {
                        "thread_id": request.thread_id
                    }
                }
            )

        # REJECT
        elif request.decision == "reject":

            response = email_agent.invoke(
                Command(
                    resume={
                        "decisions": [
                            {
                                "type": "reject"
                            }
                        ]
                    }
                ),
                config={
                    "configurable": {
                        "thread_id": request.thread_id
                    }
                }
            )

        else:

            raise HTTPException(
                status_code=400,
                detail="Invalid decision"
            )

        return {
            "status": "completed",
            "response": response
        }

    except Exception as e:

        logger.error(
            f"Approval error: {e}",
            exc_info=True
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
if __name__ == "__main__":
    
    uvicorn.run("backend:app", port=8000, host="127.0.0.1", reload=False)
