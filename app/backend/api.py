from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.core.ai_agent import get_response_from_ai_agents
from app.config.settings import settings
from typing import List
from app.common.logger import get_logger

logger = get_logger(__name__)
app = FastAPI(title="Multi-AI Agent")

class RequestState(BaseModel):
    model_name: str
    query: List[str]
    allow_search: bool = False
    system_prompt: str = ""

@app.post("/chat")
def chat_endpoint(request: RequestState):
    logger.info(f"Received request for model: {request.model_name}")

    if request.model_name not in settings.allowed_model_names:
        logger.error(f"Model {request.model_name} is not allowed.")
        raise HTTPException(status_code=400, detail="Model not allowed.")

    try:
        response = get_response_from_ai_agents(
            llm_id=request.model_name,
            query=request.query,
            allow_search=request.allow_search,
            system_prompt=request.system_prompt
        )
        logger.info(f"Response generated successfully for model: {request.model_name}") 
        
        return {"response": response}
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
