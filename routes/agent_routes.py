from fastapi import FastAPI, status, HTTPException, APIRouter
from pydantic import BaseModel
from database import agent_db

route = APIRouter()
agent_instance = agent_db.DB_Agent()

class CreateAgent(BaseModel):
    name:str
    speciality:str
    agent_rank:str

@route.post('/agents', status_code=status.HTTP_201_CREATED)
def create_agent(agent:CreateAgent):
    agent_dict = agent.model_dump()
    try:
        created = agent_instance.create_agent(agent_dict)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return created


@route.get('/agents')
def get_all_agents():
    return agent_instance.get_all_agents()