from fastapi import FastAPI, status, HTTPException, APIRouter
from pydantic import BaseModel
from database import mission_db, agent_db
import vlidation_layer as vlidation_layer
from logs import logger

route = APIRouter()
agent_instance = agent_db.DB_Agent()
mission_instance = mission_db.DB_Mission()
validate = vlidation_layer.ValidateData()
my_logger = logger.get_logger(__name__)

class CreateAndUpdateMission(BaseModel):
    title:str
    description:str
    location:str
    difficulty:int
    importance:int

@route.post('/missions', status_code=status.HTTP_201_CREATED)
def create_mission(mission:CreateAndUpdateMission):
    my_logger.info('in endpoint create mission')
    mission_dict = mission.model_dump()
    try:
        my_logger.info('accessing db to add mission')
        created = mission_instance.create_mission(mission_dict)
    except ValueError as e:
        my_logger.error('importance and difficulty shoulde by only 1-10')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    my_logger.info('mission addedd successfully')
    return {'message': 'mission Created', 'data':created}


@route.get('/missions')
def get_all_missions():
    my_logger.info('in endpoint get_all_missions')
    my_logger.info('accessing db to get all missions')
    my_logger.info('returning all missions')
    missions = mission_instance.get_all_missions()
    if missions:
        return {'message':'all missions', 'data':mission_instance.get_all_missions()}
    return missions


@route.get('/missions/{id}')
def get_mission_by_id(id:int):
    my_logger.info('in endpoint get_mission_by_id')
    my_logger.info('accessing db to get mission')
    mission = mission_instance.get_mission_by_id(id)
    if not mission:
        my_logger.error('mission does not exist')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    my_logger.info('returning mission')
    return {'message':'mission', 'data':mission_instance.get_mission_by_id(id)}


@route.put('/missions/{id}/assign/{agent_id}')
def assign_mission_to_agent(id:int, agent_id:int):
    my_logger.info('in endpoint assign_mission_to_agent')
    try:
        my_logger.info('accessing db to validate mission and agent')
        can_assign = validate.check_assign_mission(id, agent_id)
    except KeyError as e:
        my_logger.error('mission or agent does not exist')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        my_logger.error('data not currect for assignment')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    my_logger.info('accessing db to assign mission to agent')
    mission_instance.assign_mission(id, agent_id)
    my_logger.info('mission assigned')
    return 'ASSIGNED'


@route.put('/missions/{id}/start')
def start_mission(id:int):
            my_logger.info('in endpoint start_mission')
            try:
                my_logger.info('accessing db to validate mission')
                can_start = validate.check_start_mission(id)
            except KeyError as e:
                my_logger.error('mission does not exist')
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            except ValueError as e:
                my_logger.error('data not currect for mission')
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

            if can_start:
                my_logger.info('accessing db to assign mission to agent')
                mission_instance.update_mission_status(id, 'IN_PROGRESS')
                my_logger.info('mission started')
                return 'IN_PROGRESS'
            
            my_logger.error('data not currect for mission')
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@route.put('/missions/{id}/complete')
def complete_mission(id:int):
            my_logger.info('in endpoint complete_mission')
            try:
                my_logger.info('accessing db to validate mission')
                can_complete = validate.check_finish_mission(id)
            except KeyError as e:
                my_logger.error('mission does not exist')
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            except ValueError as e:
                my_logger.error('data not currect for mission')
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

            if can_complete:
                my_logger.info('accessing db to COMPLETED mission')
                mission_instance.update_mission_status(id, 'COMPLETED')
                agent_instance.increment_completed(mission_instance.get_mission_by_id(id)['assigned_agent_id'])
                my_logger.info('mission COMPLETED')
                return 'COMPLETED'
            my_logger.error('data not currect for mission')            
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@route.put('/missions/{id}/fail')
def fail_mission(id:int):
            my_logger.info('in endpoint fail_mission')
            try:
                my_logger.info('accessing db to validate mission')
                can_fail = validate.check_finish_mission(id)
            except KeyError as e:
                my_logger.error('mission does not exist')
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            except ValueError as e:
                my_logger.error('data not currect for mission')
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

            if can_fail:
                my_logger.info('accessing db to FAILED mission')
                mission_instance.update_mission_status(id, 'FAILED')
                agent_instance.increment_failed(mission_instance.get_mission_by_id(id)['assigned_agent_id'])
                my_logger.info('mission FAILED')
                return 'FAILED'
            my_logger.error('data not currect for mission')
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@route.put('/missions/{id}/cancel')
def cancel_mission(id:int):
            my_logger.info('in endpoint fail_mission')
            try:
                my_logger.info('accessing db to validate mission')
                can_cancel = validate.check_cancel_mission(id)
            except KeyError as e:
                my_logger.error('mission does not exist')
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            except ValueError as e:
                my_logger.error('data not currect for mission')
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

            if can_cancel:
                my_logger.info('accessing db to CANCELLED mission')
                mission_instance.update_mission_status(id, 'CANCELLED')
                my_logger.info('mission CANCELLED')
                return 'CANCELLED'
            my_logger.error('data not currect for mission')
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
           
           
                 
