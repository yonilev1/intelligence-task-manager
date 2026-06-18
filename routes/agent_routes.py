from fastapi import FastAPI, status, HTTPException, APIRouter
from pydantic import BaseModel
from database import agent_db
import vlidation_layer

route = APIRouter()
agent_instance = agent_db.DB_Agent()
validate = vlidation_layer.ValidateData()

class CreateAndUpdateAgent(BaseModel):
    name:str
    speciality:str
    agent_rank:str


@route.post('/agents', status_code=status.HTTP_201_CREATED)
def create_agent(agent:CreateAndUpdateAgent):
    agent_dict = agent.model_dump()
    try:
        created = agent_instance.create_agent(agent_dict)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return {'message': 'Agent Created', 'data':created}


@route.get('/agents')
def get_all_agents():
    return agent_instance.get_all_agents()


@route.get('/agents/{id}')
def get_agent_by_id(id:int):
    agent = agent_instance.get_agent_by_id(id)
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return agent


@route.put('/agents/{id}')
def update_agent(id:int, agent:CreateAndUpdateAgent):
    if not validate.check_id_exsits(id, 'agents'):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    agent_dict = agent.model_dump()
    try:
        updated = agent_instance.update_agent(id, agent_dict)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@route.put('/agents/{id}/deactivate')
def deactivate_agent(id:int):
    if not validate.check_id_exsits(id, 'agents'):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    agent_instance.deactivate_agent(id)