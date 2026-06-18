from fastapi import FastAPI, status, HTTPException, APIRouter
from pydantic import BaseModel
from database import mission_db, agent_db
import vlidation_layer

route = APIRouter()
agent_instance = agent_db.DB_Agent()
mission_instance = mission_db.DB_Mission()
validate = vlidation_layer.ValidateData()

class CreateAndUpdateMission(BaseModel):
    title:str
    description:str
    location:str
    difficulty:int
    importance:int

@route.post('/missions', status_code=status.HTTP_201_CREATED)
def create_mission(mission:CreateAndUpdateMission):
    mission_dict = mission.model_dump()
    try:
        created = mission_instance.create_mission(mission_dict)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return {'message': 'mission Created', 'data':created}


@route.get('/missions')
def get_all_missions():
    return {'message':'all missions', 'data':mission_instance.get_all_missions()}


@route.get('/missions/{id}')
def get_mission_by_id(id:int):
    mission = mission_instance.get_mission_by_id(id)
    if not mission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {'message':'mission', 'data':mission_instance.get_mission_by_id(id)}


@route.put('/missions/{id}/assign/{agent_id}')
def assign_mission_to_agent(id:int, agent_id:int):
    try:
        can_assign = validate.check_assign_mission(id, agent_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    mission_instance.assign_mission(id, agent_id)
    return 'ASSIGNED'


@route.put('/missions/{id}/start')
def start_mission(id:int):
            try:
                can_start = validate.check_start_mission(id)
            except KeyError as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            except ValueError as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

            if can_start:
                mission_instance.update_mission_status(id, 'IN_PROGRESS')
                return 'IN_PROGRESS'
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@route.put('/missions/{id}/complete')
def complete_mission(id:int):
            try:
                can_complete = validate.check_finish_mission(id)
            except KeyError as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            except ValueError as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

            if can_complete:
                mission_instance.update_mission_status(id, 'COMPLETED')
                agent_instance.increment_completed(mission_instance.get_mission_by_id(id)['assigned_agent_id'])
                return 'COMPLETED'
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@route.put('/missions/{id}/fail')
def fail_mission(id:int):
            try:
                can_fail = validate.check_finish_mission(id)
            except KeyError as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            except ValueError as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

            if can_fail:
                mission_instance.update_mission_status(id, 'FAILED')
                agent_instance.increment_failed(mission_instance.get_mission_by_id(id)['assigned_agent_id'])
                return 'FAILED'
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@route.put('/missions/{id}/cancel')
def cancel_mission(id:int):
            try:
                can_cancel = validate.check_cancel_mission(id)
            except KeyError as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            except ValueError as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

            if can_cancel:
                mission_instance.update_mission_status(id, 'CANCELLED')
                return 'CANCELLED'
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
           
           
                 
