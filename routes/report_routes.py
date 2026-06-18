from fastapi import FastAPI, status, HTTPException, APIRouter
from pydantic import BaseModel
from database import mission_db, agent_db

route = APIRouter()
agent_instance = agent_db.DB_Agent()
mission_instance = mission_db.DB_Mission()

@route.get('/reports/summary')
def get_report_summary():
    return {'message':'report summary',
            'data': {"active_agents_count" : agent_instance.count_active_agents(),
            "total_missions" : mission_instance.count_all_missions(),
            "open_missions" : mission_instance.count_open_missions(),
            "completed_missions" : mission_instance.count_completed_missions(),
            "failed_missions" : mission_instance.count_failed_missions(),
            "critical_missions" : mission_instance.count_critical_missions()}}


@route.get('/reports/missions-by-status')
def get_missions_by_status():
    return {'message':'mission by status',
            'data': {"open": mission_instance.count_by_status('IN_PROGRESS') + mission_instance.count_by_status('ASSIGNED'), 
                     "in_progress": mission_instance.count_by_status('IN_PROGRESS'), 
                     "completed": mission_instance.count_by_status('COMPLETED'), 
                     "failed": mission_instance.count_by_status('FAILED'), 
                     "canceled": mission_instance.count_by_status('CANCELLED')}}


@route.get('/reports/top-agent')
def get_top_agent():
    top_agent_id = mission_instance.get_top_agent()
    agent = agent_instance.get_agent_by_id(top_agent_id)
    if agent:
        return {'message':'top agent', 'data': agent}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No top agent')