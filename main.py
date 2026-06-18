from fastapi import FastAPI, status, HTTPException
from routes import agent_routes, mission_routes, report_routes

app = FastAPI()
app.include_router(agent_routes.route)