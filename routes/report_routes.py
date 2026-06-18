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
            "critical_missions" : mission_instance.count_critical_missions()} }