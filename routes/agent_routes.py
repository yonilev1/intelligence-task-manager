from fastapi import FastAPI, status, HTTPException, APIRouter
from pydantic import BaseModel
from database import agent_db
import vlidation_layer as vlidation_layer
from logs import logger

route = APIRouter()
agent_instance = agent_db.DB_Agent()
validate = vlidation_layer.ValidateData()
my_logger = logger.get_logger(__name__)

class CreateAndUpdateAgent(BaseModel):
    name:str
    speciality:str
    agent_rank:str


@route.post('/agents', status_code=status.HTTP_201_CREATED)
def create_agent(agent:CreateAndUpdateAgent):
    my_logger.info('in endpoint create agent')
    agent_dict = agent.model_dump()
    try:
        my_logger.info('accessing db to add agent')
        created = agent_instance.create_agent(agent_dict)
    except ValueError as e:
        my_logger.error('rank shoulde by only one of - [Junior, Senior, Commander]')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'rank shoulde by only one of - [Junior, Senior, Commander]')
    my_logger.info('agent addedd successfully')
    return {'message': 'Agent Created', 'data':created}


@route.get('/agents')
def get_all_agents():
    my_logger.info('in endpoint get_all_agents')
    my_logger.info('accessing db to get all agent')
    my_logger.info('returning all agents')
    agents = agent_instance.get_all_agents()
    if agents:
        return {'message': 'All agents', 'data':agents}
    return agents


@route.get('/agents/{id}')
def get_agent_by_id(id:int):
    my_logger.info('in endpoint get_agent_by_id')
    my_logger.info('accessing db to get agent')
    agent = agent_instance.get_agent_by_id(id)
    if not agent:
        my_logger.error('agent does not exist')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Agent Not Found')
    my_logger.info('returning agent')
    return {'message': 'agent', 'data':agent}


@route.put('/agents/{id}')
def update_agent(id:int, agent:CreateAndUpdateAgent):
    my_logger.info('in endpoint update_agent')
    my_logger.info('accessing db to validate agent')
    if not validate.check_id_exsits(id, 'agents'):
        my_logger.error('agent does not exist')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Agent Not Found')
    agent_dict = agent.model_dump()
    try:
        my_logger.info('accessing db to update agent')
        updated = agent_instance.update_agent(id, agent_dict)
    except ValueError as e:
        my_logger.error('data not currect for update')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'rank shoulde by only one of - [Junior, Senior, Commander]')
    
    my_logger.info('updated agent')


@route.put('/agents/{id}/deactivate')
def deactivate_agent(id:int):
    my_logger.info('in endpoint deactivate_agent')
    my_logger.info('accessing db to validate agent')
    if not validate.check_id_exsits(id, 'agents'):
        my_logger.error('agent does not exist')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Agent Not Found')
    my_logger.info('accessing db to deactivate agent')
    agent_instance.deactivate_agent(id)
    my_logger.info('deactivated agent')


@route.get('/agents/{id}/performance')
def get_agent_performance(id:int):
    my_logger.info('in endpoint get_agent_performance')
    my_logger.info('accessing db to validate agent')
    if not validate.check_id_exsits(id, 'agents'):
        my_logger.error('agent does not exist')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Agent Not Found')
    my_logger.info('return agent performance')
    return {'message':'agents performance', 'data':agent_instance.get_agent_performance(id)}