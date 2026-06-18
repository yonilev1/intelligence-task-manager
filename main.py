from fastapi import FastAPI, status, HTTPException
from routes import agent_routes, mission_routes, report_routes
import uvicorn

app = FastAPI()
app.include_router(agent_routes.route)
app.include_router(mission_routes.route)


if __name__=="__main__":
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=False)